#!/usr/bin/env python3
"""
Smart Contract Deployment Script
Stage 2: Deploy and interact with Solidity contracts
"""

import json
import os
from typing import Dict, Optional
from web3 import Web3
from eth_account import Account


class ContractDeployer:
    """Helper class to deploy and interact with smart contracts."""
    
    def __init__(self, provider_url: str = "http://127.0.0.1:8545"):
        """
        Initialize deployer.
        
        Args:
            provider_url (str): RPC provider URL.
        """
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        
        if not self.w3.is_connected():
            print(f"Warning: Cannot connect to {provider_url}")
        else:
            print(f"Connected to provider: {provider_url}")
    
    def compile_contract(self, contract_path: str) -> Optional[Dict]:
        """
        Compile Solidity contract using solcx.
        
        Args:
            contract_path (str): Path to .sol file.
        
        Returns:
            Dict: Compiled contract with ABI and bytecode.
        """
        try:
            from solcx import compile_source, set_solc_version
            
            # Read contract file
            with open(contract_path, 'r') as f:
                source_code = f.read()
            
            # Set solc version
            set_solc_version("0.8.19")
            
            # Compile
            compiled = compile_source(
                source_code,
                solc_version="0.8.19",
                output_values=["abi", "bin"]
            )
            
            # Get first contract
            contract_key = list(compiled.keys())[0]
            contract_data = compiled[contract_key]
            
            return {
                "abi": contract_data['abi'],
                "bytecode": contract_data['bin']
            }
            
        except ImportError:
            print("Error: solcx not installed!")
            print("Install with: pip install py-solc-x")
            print("Then install solc: python3 -m solcx.install v0.8.19")
            return None
        except FileNotFoundError as e:
            print(f"Error: Could not find solc binary. {e}")
            print("Install with: python3 -m solcx.install v0.8.19")
            return None
        except Exception as e:
            print(f"Error: Failed to compile contract: {e}")
            return None
    
    def _get_test_abi(self) -> list:
        """Get test ABI for SimpleGreeter contract."""
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
                "stateMutability": "nonpayable",
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
    
    def _get_test_bytecode(self) -> str:
        """Get test bytecode."""
        return "0x6080604052"
    
    def deploy_contract(self, contract_name: str, constructor_args: list,
                       deployer_address: str, private_key: str) -> Dict:
        """
        Deploy contract to blockchain.
        
        Args:
            contract_name (str): Contract name.
            constructor_args (list): Constructor arguments.
            deployer_address (str): Deployer address.
            private_key (str): Deployer private key.
        
        Returns:
            Dict: Deployment info with address and tx hash.
        """
        try:
            compiled = self.compile_contract("stage2/smart_contract/SimpleGreeter.sol")
            
            if not compiled:
                return {"error": "Failed to compile contract"}
            
            abi = compiled["abi"]
            bytecode = compiled["bytecode"]
            
            contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
            
            deployer_address = Web3.to_checksum_address(deployer_address)
            nonce = self.w3.eth.get_transaction_count(deployer_address)
            
            constructor = contract.constructor(*constructor_args)
            
            tx = constructor.build_transaction({
                "from": deployer_address,
                "nonce": nonce,
                "gas": 1000000,
                "gasPrice": self.w3.eth.gas_price
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
            
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            print(f"\nTransaction sent. Hash: {tx_hash.hex()}")
            print("Waiting for confirmation...")
            
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            contract_address = receipt["contractAddress"]
            
            return {
                "success": True,
                "contract_address": contract_address,
                "tx_hash": tx_hash.hex(),
                "deployer": deployer_address,
                "block_number": receipt["blockNumber"],
                "gas_used": receipt["gasUsed"],
                "abi": abi
            }
        
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_contract(self, contract_address: str, abi: list) -> Dict:
        """
        Get reference to deployed contract.
        
        Args:
            contract_address (str): Contract address.
            abi (list): Contract ABI.
        
        Returns:
            Dict: Contract instance and available methods.
        """
        try:
            contract_address = Web3.to_checksum_address(contract_address)
            contract = self.w3.eth.contract(address=contract_address, abi=abi)
            
            return {
                "success": True,
                "contract": contract,
                "address": contract_address,
                "functions": list(contract.functions)
            }
        
        except Exception as e:
            return {"error": str(e), "success": False}


def main():
    """Main function for contract deployment demo."""
    print("="*60)
    print("Smart Contract Deployment - Stage 2")
    print("="*60 + "\n")
    
    deployer = ContractDeployer()
    
    print("\nOptions:")
    print("1. Deploy SimpleGreeter")
    print("2. Check deployment")
    print("3. Load contract")
    print("4. Exit")
    
    choice = input("\nSelect (1-4): ").strip()
    
    if choice == "1":
        print("\n" + "="*60)
        print("Deploy SimpleGreeter")
        print("="*60 + "\n")
        
        greeting = input("Initial greeting (default: 'Hello'): ").strip()
        greeting = greeting or "Hello"
        
        addr = input("Deployer address: ").strip()
        pk = input("Private key: ").strip()
        
        print("\nDeploying...")
        result = deployer.deploy_contract(
            "SimpleGreeter",
            [greeting],
            addr,
            pk
        )
        
        if result.get("success"):
            print("\nSuccess!")
            print(f"Address: {result['contract_address']}")
            print(f"Tx: {result['tx_hash']}")
            print(f"Block: {result['block_number']}")
            
            deployment = {
                "name": "SimpleGreeter",
                "address": result["contract_address"],
                "tx_hash": result["tx_hash"],
                "deployer": result["deployer"],
                "abi": result["abi"]
            }
            
            with open("deployment.json", "w") as f:
                json.dump(deployment, f, indent=2)
            
            print("\nSaved to deployment.json")
        else:
            print(f"\nError: {result.get('error')}")
    
    elif choice == "2":
        if os.path.exists("deployment.json"):
            with open("deployment.json", "r") as f:
                print(json.dumps(json.load(f), indent=2))
        else:
            print("No deployment found")
    
    elif choice == "3":
        address = input("Contract address: ").strip()
        print(f"Loaded: {address}")
    
    else:
        print("Exit")


if __name__ == "__main__":
    main()
