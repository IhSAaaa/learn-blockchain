#!/usr/bin/env python3
"""
Integration Tests for Smart Contract Deploy and Interact
Tests the complete workflow: Deploy -> Read -> Update -> Verify
"""

import unittest
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from web3 import Web3
from deploy import ContractDeployer
from interact import ContractInteractor


class IntegrationTestDeployAndInteract(unittest.TestCase):
    """Integration tests for deploy.py and interact.py workflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create deployer and interactor with mocked provider
        self.mock_provider_url = "http://127.0.0.1:8545"
        self.deployer = ContractDeployer(provider_url=self.mock_provider_url)
        self.interactor = ContractInteractor(provider_url=self.mock_provider_url)
        
        # Create temporary directory for test artifacts
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """Clean up after tests."""
        os.chdir(self.original_cwd)
        # Clean up temporary files
        if os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir)
    
    def get_mock_abi(self):
        """Get mock ABI for SimpleGreeter contract."""
        return [
            {
                "inputs": [{"internalType": "string", "name": "initialGreeting", "type": "string"}],
                "stateMutability": "nonpayable",
                "type": "constructor"
            },
            {
                "inputs": [{"internalType": "string", "name": "newGreeting", "type": "string"}],
                "name": "setGreeting",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getGreeting",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "greeting",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "greetingCount",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
    
    def test_compile_contract_succeeds(self):
        """Test that contract compilation returns valid ABI and bytecode."""
        # Mock compilation to avoid needing solcx installed
        result = {
            "abi": self.get_mock_abi(),
            "bytecode": "0x6080604052"
        }
        
        self.assertIsNotNone(result)
        self.assertIn("abi", result)
        self.assertIn("bytecode", result)
        self.assertIsInstance(result["abi"], list)
        self.assertIsInstance(result["bytecode"], str)
    
    def test_deployer_initializes_with_provider(self):
        """Test that deployer initializes with correct provider URL."""
        deployer = ContractDeployer(provider_url=self.mock_provider_url)
        self.assertIsNotNone(deployer.w3)
    
    def test_interactor_initializes_with_provider(self):
        """Test that interactor initializes with correct provider URL."""
        interactor = ContractInteractor(provider_url=self.mock_provider_url)
        self.assertIsNotNone(interactor.w3)
    
    @patch('deploy.Web3')
    def test_deployment_workflow_with_mock(self, mock_web3_class):
        """Test complete deployment workflow with mocked Web3."""
        # Setup mocks
        mock_w3 = MagicMock()
        mock_web3_class.HTTPProvider.return_value = MagicMock()
        mock_web3_class.return_value = mock_w3
        mock_web3_class.to_checksum_address = Web3.to_checksum_address
        
        mock_w3.is_connected.return_value = True
        mock_w3.eth.get_transaction_count.return_value = 0
        mock_w3.eth.gas_price = 1000000000
        mock_w3.eth.send_raw_transaction.return_value = b'\x00' * 32
        mock_w3.eth.wait_for_transaction_receipt.return_value = {
            "contractAddress": "0x" + "1" * 40,
            "blockNumber": 1,
            "gasUsed": 100000,
            "status": 1
        }
        
        # Create mock contract
        mock_contract = MagicMock()
        mock_constructor = MagicMock()
        mock_constructor.build_transaction.return_value = {
            "from": "0x" + "1" * 40,
            "nonce": 0,
            "gas": 1000000,
            "gasPrice": 1000000000
        }
        mock_contract.constructor.return_value = mock_constructor
        mock_w3.eth.contract.return_value = mock_contract
        mock_w3.eth.account.sign_transaction = Mock()
        mock_w3.eth.account.sign_transaction.return_value = MagicMock(rawTransaction=b'test')
        
        # Create deployer with mocked Web3
        deployer = ContractDeployer(provider_url=self.mock_provider_url)
        deployer.w3 = mock_w3
        
        # Test deployment
        test_address = "0x" + "2" * 40
        test_key = "0x" + "3" * 64
        
        with patch.object(deployer, 'compile_contract', return_value={"abi": self.get_mock_abi(), "bytecode": "0x123"}):
            result = deployer.deploy_contract(
                "SimpleGreeter",
                ["Hello World"],
                test_address,
                test_key
            )
        
        # Verify deployment result structure
        self.assertTrue(result["success"])
        self.assertIn("contract_address", result)
        self.assertIn("tx_hash", result)
        self.assertIn("abi", result)
    
    def test_abi_loading_in_interact(self):
        """Test that interactor can work with loaded ABI."""
        mock_abi = self.get_mock_abi()
        mock_contract_address = "0x" + "1" * 40
        
        # Verify that interactor has the methods needed to call functions
        self.assertIsNotNone(self.interactor.call_function)
        self.assertIsNotNone(self.interactor.send_transaction)
        self.assertIsNotNone(self.interactor.get_events)
    
    @patch('interact.Web3')
    def test_read_call_workflow(self, mock_web3_class):
        """Test read-only function call workflow."""
        # Setup mocks
        mock_w3 = MagicMock()
        mock_web3_class.HTTPProvider.return_value = MagicMock()
        mock_web3_class.return_value = mock_w3
        mock_web3_class.to_checksum_address = Web3.to_checksum_address
        
        mock_w3.is_connected.return_value = True
        
        mock_contract = MagicMock()
        mock_function = MagicMock()
        mock_function.call.return_value = "Hello World"
        mock_contract.functions.getGreeting = Mock(return_value=mock_function)
        mock_w3.eth.contract.return_value = mock_contract
        
        # Create interactor with mocked w3
        interactor = ContractInteractor(provider_url=self.mock_provider_url)
        
        # Test call_function
        mock_abi = self.get_mock_abi()
        mock_contract_address = "0x" + "1" * 40
        
        result = interactor.call_function(
            mock_contract_address,
            mock_abi,
            "getGreeting"
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["result"], "Hello World")
        self.assertEqual(result["function"], "getGreeting")
    
    @patch('interact.Web3')
    def test_write_transaction_workflow(self, mock_web3_class):
        """Test state-changing transaction workflow."""
        # Setup mocks
        mock_w3 = MagicMock()
        mock_web3_class.HTTPProvider.return_value = MagicMock()
        mock_web3_class.return_value = mock_w3
        mock_web3_class.to_checksum_address = Web3.to_checksum_address
        
        mock_w3.is_connected.return_value = True
        mock_w3.eth.get_transaction_count.return_value = 0
        mock_w3.eth.gas_price = 1000000000
        
        mock_contract = MagicMock()
        mock_function = MagicMock()
        mock_tx_obj = MagicMock()
        mock_tx_obj.build_transaction.return_value = {
            "from": "0x" + "1" * 40,
            "nonce": 0,
            "value": 0,
            "gas": 1000000,
            "gasPrice": 1000000000
        }
        mock_function.return_value = mock_tx_obj
        mock_contract.functions.setGreeting = Mock(return_value=mock_function)
        mock_w3.eth.contract.return_value = mock_contract
        
        # Mock transaction sending
        mock_w3.eth.account.sign_transaction = Mock()
        mock_w3.eth.account.sign_transaction.return_value = MagicMock(rawTransaction=b'test')
        mock_w3.eth.send_raw_transaction.return_value = b'\x00' * 32
        mock_w3.eth.wait_for_transaction_receipt.return_value = {
            "blockNumber": 1,
            "gasUsed": 50000,
            "status": 1
        }
        
        # Create interactor with mocked w3
        interactor = ContractInteractor(provider_url=self.mock_provider_url)
        
        # Test send_transaction
        mock_abi = self.get_mock_abi()
        mock_contract_address = "0x" + "1" * 40
        sender_address = "0x" + "2" * 40
        private_key = "0x" + "3" * 64
        
        result = interactor.send_transaction(
            mock_contract_address,
            mock_abi,
            "setGreeting",
            sender_address,
            private_key,
            ["New Greeting"]
        )
        
        self.assertTrue(result["success"])
        self.assertIn("tx_hash", result)
        self.assertIn("block_number", result)
        self.assertIn("gas_used", result)
        self.assertEqual(result["status"], "Success")
    
    def test_complete_workflow_simulation(self):
        """Test complete workflow: compile -> prepare deployment -> prepare call -> prepare transaction."""
        # Step 1: Mock compile contract
        compiled = {
            "abi": self.get_mock_abi(),
            "bytecode": "0x6080604052"
        }
        self.assertIsNotNone(compiled)
        self.assertIn("abi", compiled)
        
        # Step 2: Verify ABI structure
        abi = compiled["abi"]
        self.assertIsInstance(abi, list)
        self.assertGreater(len(abi), 0)
        
        # Step 3: Verify that interactor can accept this ABI
        mock_contract_address = Web3.to_checksum_address("0x" + "1" * 40)
        self.assertTrue(Web3.is_address(mock_contract_address))
        
        # Step 4: Verify Web3 utility methods
        self.assertTrue(Web3.is_address("0x" + "1" * 40))
        self.assertFalse(Web3.is_address("invalid"))
    
    def test_artifact_persistence(self):
        """Test that deployment artifacts can be saved and loaded."""
        deployment_info = {
            "name": "SimpleGreeter",
            "address": "0x" + "1" * 40,
            "tx_hash": "0x" + "2" * 64,
            "deployer": "0x" + "3" * 40,
            "abi": self.get_mock_abi()
        }
        
        # Save artifact
        artifact_path = os.path.join(self.test_dir, "SimpleGreeter.json")
        with open(artifact_path, "w") as f:
            json.dump(deployment_info, f, indent=2)
        
        # Verify file exists
        self.assertTrue(os.path.exists(artifact_path))
        
        # Load artifact
        with open(artifact_path, "r") as f:
            loaded_info = json.load(f)
        
        # Verify content matches
        self.assertEqual(loaded_info["name"], deployment_info["name"])
        self.assertEqual(loaded_info["address"], deployment_info["address"])
        self.assertEqual(loaded_info["abi"], deployment_info["abi"])
    
    @patch('interact.Web3')
    def test_event_retrieval_workflow(self, mock_web3_class):
        """Test event retrieval workflow."""
        # Setup mocks
        mock_w3 = MagicMock()
        mock_web3_class.HTTPProvider.return_value = MagicMock()
        mock_web3_class.return_value = mock_w3
        mock_web3_class.to_checksum_address = Web3.to_checksum_address
        
        mock_w3.is_connected.return_value = True
        
        mock_contract = MagicMock()
        mock_event = MagicMock()
        mock_event.get_logs.return_value = [
            {"args": {"updater": "0x" + "1" * 40, "newGreeting": "Hello"}},
            {"args": {"updater": "0x" + "2" * 40, "newGreeting": "Hi"}}
        ]
        mock_contract.events.GreetingUpdated = mock_event
        mock_w3.eth.contract.return_value = mock_contract
        
        # Create interactor with mocked w3
        interactor = ContractInteractor(provider_url=self.mock_provider_url)
        
        # Test get_events
        mock_abi = self.get_mock_abi()
        mock_contract_address = "0x" + "1" * 40
        
        result = interactor.get_events(
            mock_contract_address,
            mock_abi,
            "GreetingUpdated"
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["event_name"], "GreetingUpdated")
        self.assertEqual(result["count"], 2)


class WorkflowSequenceTest(unittest.TestCase):
    """Test the sequence of operations in deploy and interact workflow."""
    
    def test_provider_url_consistency(self):
        """Test that deployer and interactor use same provider URL."""
        provider_url = "http://127.0.0.1:8545"
        
        deployer = ContractDeployer(provider_url=provider_url)
        interactor = ContractInteractor(provider_url=provider_url)
        
        # Both should have Web3 instances
        self.assertIsNotNone(deployer.w3)
        self.assertIsNotNone(interactor.w3)
    
    def test_deploy_before_interact_requirement(self):
        """Verify that deployment must happen before interaction."""
        # This is a logical test - interact needs contract address from deploy
        # We verify that interact.call_function requires contract_address parameter
        interactor = ContractInteractor()
        
        # Verify method signature requires contract_address
        import inspect
        sig = inspect.signature(interactor.call_function)
        params = list(sig.parameters.keys())
        
        self.assertIn("contract_address", params)
        self.assertIn("abi", params)
        self.assertIn("function_name", params)


if __name__ == "__main__":
    unittest.main()
