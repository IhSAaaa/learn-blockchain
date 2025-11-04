#!/usr/bin/env python3
"""
Smart Contract Interaction Script
Stage 2: Call contract functions and read state
"""

import json
from typing import Dict
from web3 import Web3
from eth_account import Account


class ContractInteractor:
    """Helper class to interact with deployed smart contracts."""
    
    def __init__(self, provider_url: str = "http://127.0.0.1:8545"):
        """
        Initialize the contract interactor.
        
        Args:
            provider_url: RPC provider URL endpoint.
        """
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        
        if not self.w3.is_connected():
            print(f"Warning: Cannot connect to {provider_url}")
        else:
            print(f"Connected to {provider_url}")
    
    def call_function(self, contract_address: str, abi: list,
                     function_name: str, args: list = None) -> Dict:
        """
        Call a read-only function (view/pure) from the contract.
        
        Args:
            contract_address: Target contract address.
            abi: Contract ABI.
            function_name: Name of the function to call.
            args: Function arguments.
        
        Returns:
            Dictionary with success status and result.
        """
        try:
            contract_address = Web3.to_checksum_address(contract_address)
            contract = self.w3.eth.contract(address=contract_address, abi=abi)
            
            function = getattr(contract.functions, function_name)
            
            if args:
                result = function(*args).call()
            else:
                result = function().call()
            
            return {
                "success": True,
                "result": result,
                "function": function_name
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_transaction(self, contract_address: str, abi: list,
                        function_name: str, from_address: str,
                        private_key: str, args: list = None,
                        value: int = 0) -> Dict:
        """
        Send a state-changing transaction to the contract.
        
        Args:
            contract_address: Target contract address.
            abi: Contract ABI.
            function_name: Name of the function to call.
            from_address: Sender address.
            private_key: Sender's private key.
            args: Function arguments.
            value: ETH value to send (in wei).
        
        Returns:
            Dictionary with transaction receipt details.
        """
        try:
            contract_address = Web3.to_checksum_address(contract_address)
            from_address = Web3.to_checksum_address(from_address)
            
            contract = self.w3.eth.contract(address=contract_address, abi=abi)
            function = getattr(contract.functions, function_name)
            
            nonce = self.w3.eth.get_transaction_count(from_address)
            
            if args:
                tx = function(*args).build_transaction({
                    "from": from_address,
                    "nonce": nonce,
                    "value": value,
                    "gas": 1000000,
                    "gasPrice": self.w3.eth.gas_price
                })
            else:
                tx = function().build_transaction({
                    "from": from_address,
                    "nonce": nonce,
                    "value": value,
                    "gas": 1000000,
                    "gasPrice": self.w3.eth.gas_price
                })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            return {
                "success": True,
                "tx_hash": tx_hash.hex(),
                "block_number": receipt["blockNumber"],
                "gas_used": receipt["gasUsed"],
                "status": "Success" if receipt["status"] else "Failed"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_events(self, contract_address: str, abi: list,
                  event_name: str, from_block: int = 0) -> Dict:
        """
        Retrieve emitted events from the contract.
        
        Args:
            contract_address: Target contract address.
            abi: Contract ABI.
            event_name: Name of the event.
            from_block: Starting block number.
        
        Returns:
            Dictionary with event logs.
        """
        try:
            contract_address = Web3.to_checksum_address(contract_address)
            contract = self.w3.eth.contract(address=contract_address, abi=abi)
            
            event = getattr(contract.events, event_name)
            events = event.get_logs(from_block=from_block)
            
            return {
                "success": True,
                "event_name": event_name,
                "count": len(events),
                "events": [dict(e) for e in events]
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}


def demo_interactive():
    """Interactive demo using deployment.json file."""
    print("="*60)
    print("Smart Contract Interaction Demo")
    print("="*60 + "\n")
    
    try:
        with open("deployment.json", "r") as f:
            deployment = json.load(f)
    except FileNotFoundError:
        print("Error: deployment.json not found")
        print("Please run deploy.py first")
        return
    
    interactor = ContractInteractor()
    contract_address = deployment["address"]
    abi = deployment["abi"]
    
    print(f"Address: {contract_address}\n")
    
    result = interactor.call_function(contract_address, abi, "getGreeting")
    if result["success"]:
        print(f"Current greeting: {result['result']}\n")
    
    while True:
        print("Options:")
        print("  1 - Read greeting")
        print("  2 - Update greeting")
        print("  3 - Exit")
        
        choice = input("\nSelect: ").strip()
        
        if choice == "1":
            result = interactor.call_function(contract_address, abi, "getGreeting")
            if result["success"]:
                print(f"Greeting: {result['result']}\n")
            else:
                print(f"Error: {result['error']}\n")
        
        elif choice == "2":
            greeting = input("New greeting: ").strip()
            address = input("Your address: ").strip()
            key = input("Private key: ").strip()
            
            result = interactor.send_transaction(
                contract_address, abi,
                "setGreeting",
                address, key,
                [greeting]
            )
            
            if result["success"]:
                print(f"\nTransaction sent")
                print(f"Hash: {result['tx_hash']}\n")
            else:
                print(f"Error: {result['error']}\n")
        
        elif choice == "3":
            break


def main():
    demo_interactive()


if __name__ == "__main__":
    main()
