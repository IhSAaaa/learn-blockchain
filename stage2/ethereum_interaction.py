#!/usr/bin/env python3
"""
Ethereum Interaction with Web3.py
Stage 2: Direct blockchain interaction and account management

This is where things get real - we're actually talking to an Ethereum node
and moving money around. Pretty cool, but also a little nerve-wracking if
you think about it too hard.
"""

import os
import json
from typing import Dict, Optional
from web3 import Web3
from eth_account import Account


class EthereumClient:
    """
    A client for poking at Ethereum blockchain stuff using Web3.py.
    
    Pretty straightforward - you give it an RPC endpoint and it does the heavy lifting
    for you. Accounts, balances, transactions, all that jazz.
    """
    
    def __init__(self, provider_url: str = "http://127.0.0.1:8545"):
        """
        Set up the client.
        
        Args:
            provider_url (str): Where the blockchain lives. Defaults to local Ganache,
                              but you can throw in an Infura or Alchemy URL if you want
        """
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.provider_url = provider_url
        
        # Trying to connect... fingers crossed
        if not self.w3.is_connected():
            print(f"Can't reach {provider_url}")
            print("Do you have Ganache running? Or maybe double-check that RPC URL?")
            print("These things happen, no biggie.")
        else:
            print(f"✓ Connected to Ethereum node: {provider_url}")
    
    def get_connection_status(self) -> Dict:
        """
        Check if we're actually connected and grab some basic network info.
        
        Useful to call this first just to make sure everything's working
        before you try to do anything fancy.
        """
        try:
            if not self.w3.is_connected():
                return {
                    "connected": False,
                    "message": "Can't reach the provider - network issue?"
                }
            
            chain_id = self.w3.eth.chain_id
            latest_block = self.w3.eth.block_number
            gas_price = self.w3.eth.gas_price
            
            # All the info you'd want to know about the network right now
            return {
                "connected": True,
                "provider": self.provider_url,
                "chain_id": chain_id,
                "latest_block": latest_block,
                "gas_price_wei": gas_price,
                "gas_price_gwei": self.w3.from_wei(gas_price, "gwei")
            }
        except Exception as e:
            return {"connected": False, "error": str(e)}
    
    def create_account(self) -> Dict:
        """
        Generate a brand new Ethereum account from scratch.
        
        This is actually pretty easy - eth_account just makes a new keypair
        for you. The address is derived from the public key. Pretty elegant, really.
        
        Returns:
            Dict with address, private key, and the account object itself
        """
        account = Account.create()
        return {
            "address": account.address,
            "private_key": account.key.hex(),
            "account": account
        }
    
    def get_balance(self, address: str) -> Dict:
        """
        Find out how much ETH someone has.
        
        Give it an address (doesn't even need to be checksummed, we handle that),
        and it tells you the balance in both Wei and actual ETH. Both formats
        are useful depending on what you're doing.
        
        Args:
            address (str): The address to check
        
        Returns:
            Dict with balance in Wei, ETH, and Gwei
        """
        if not Web3.is_address(address):
            return {"error": "That doesn't look like a valid address"}
        
        try:
            address = Web3.to_checksum_address(address)
            balance_wei = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, "ether")
            
            return {
                "address": address,
                "balance_wei": balance_wei,
                "balance_eth": float(balance_eth),
                "balance_gwei": float(self.w3.from_wei(balance_wei, "gwei"))
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_account_info(self, address: str) -> Dict:
        """
        Get the full picture of an account - balance, nonce, whether it's a contract, etc.
        
        The nonce is kinda important if you're building transactions manually.
        And checking if something's a contract vs a regular wallet? Useful to know.
        
        Args:
            address (str): The account address to look up
        
        Returns:
            Dict with all the account deets
        """
        if not Web3.is_address(address):
            return {"error": "That doesn't look like a valid address"}
        
        try:
            address = Web3.to_checksum_address(address)
            
            balance_wei = self.w3.eth.get_balance(address)
            nonce = self.w3.eth.get_transaction_count(address)
            code = self.w3.eth.get_code(address)
            
            return {
                "address": address,
                "balance_eth": float(self.w3.from_wei(balance_wei, "ether")),
                "balance_wei": balance_wei,
                "nonce": nonce,  # How many transactions this account has made
                "is_contract": len(code) > 0,  # True if there's bytecode at this address
                "code_length": len(code)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def send_transaction(self, from_address: str, to_address: str, 
                        amount_eth: float, private_key: str) -> Dict:
        """
        Send ETH from one address to another. This is the real deal.
        
        We build the transaction, sign it with the private key, send it to the network,
        and wait for it to get mined. Sounds simple, but there's a lot happening under the hood.
        
        Args:
            from_address (str): Where it's coming from
            to_address (str): Where it's going
            amount_eth (float): How much ETH to send
            private_key (str): The sender's private key (keep this secret!)
        
        Returns:
            Dict with transaction receipt or an error if things went sideways
        """
        try:
            if not Web3.is_address(from_address) or not Web3.is_address(to_address):
                return {"error": "One of those addresses doesn't look right"}
            
            from_address = Web3.to_checksum_address(from_address)
            to_address = Web3.to_checksum_address(to_address)
            
            # Get the nonce - every transaction needs this to prevent replay attacks
            nonce = self.w3.eth.get_transaction_count(from_address)
            gas_price = self.w3.eth.gas_price
            
            # Build the transaction
            tx = {
                "nonce": nonce,
                "to": to_address,
                "value": self.w3.to_wei(amount_eth, "ether"),
                "gas": 21000,  # Standard gas for a simple value transfer
                "gasPrice": gas_price,
                "chainId": self.w3.eth.chain_id
            }
            
            # Sign it with the private key
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
            # Send it off and wait for confirmation
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            return {
                "success": True,
                "tx_hash": tx_hash.hex(),
                "from": from_address,
                "to": to_address,
                "amount_eth": amount_eth,
                "gas_used": receipt["gasUsed"],
                "block_number": receipt["blockNumber"],
                "status": "Success" if receipt["status"] else "Failed"
            }
        
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_transaction_details(self, tx_hash: str) -> Dict:
        """
        Look up a transaction by its hash and grab all the juicy details.
        
        Useful for verifying that a transaction actually went through and
        seeing how much gas it actually used (vs what we estimated).
        
        Args:
            tx_hash (str): The transaction hash you want to look up
        
        Returns:
            Dict with all the transaction info
        """
        try:
            tx = self.w3.eth.get_transaction(tx_hash)
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            
            return {
                "hash": tx["hash"].hex(),
                "from": tx["from"],
                "to": tx["to"],
                "value_eth": float(self.w3.from_wei(tx["value"], "ether")),
                "gas": tx["gas"],
                "gas_price_gwei": float(self.w3.from_wei(tx["gasPrice"], "gwei")),
                "nonce": tx["nonce"],
                "block_number": receipt["blockNumber"],
                "gas_used": receipt["gasUsed"],
                "status": "Success" if receipt["status"] else "Failed"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def estimate_gas(self, from_address: str, to_address: str, 
                    amount_eth: float) -> Dict:
        """
        Try to guess how much gas a transaction will cost before actually sending it.
        
        This is kinda important because gas can get pricey. Better to know what you're
        in for before you commit. It's not always 100% accurate but it's usually pretty close.
        
        Args:
            from_address (str): Sender
            to_address (str): Recipient
            amount_eth (float): Amount in ETH
        
        Returns:
            Dict with gas estimate, current gas price, and estimated total cost
        """
        try:
            if not Web3.is_address(from_address) or not Web3.is_address(to_address):
                return {"error": "One of those addresses doesn't look right"}
            
            from_address = Web3.to_checksum_address(from_address)
            to_address = Web3.to_checksum_address(to_address)
            
            gas_estimate = self.w3.eth.estimate_gas({
                "from": from_address,
                "to": to_address,
                "value": self.w3.to_wei(amount_eth, "ether")
            })
            
            gas_price = self.w3.eth.gas_price
            gas_price_gwei = float(self.w3.from_wei(gas_price, "gwei"))
            tx_fee_eth = float(self.w3.from_wei(gas_estimate * gas_price, "ether"))
            
            return {
                "gas_estimate": gas_estimate,
                "gas_price_gwei": gas_price_gwei,
                "estimated_fee_eth": tx_fee_eth,
                "total_eth": amount_eth + tx_fee_eth
            }
        except Exception as e:
            return {"error": str(e)}


def main():
    """
    Just messing around with the EthereumClient to see what it can do.
    
    This script walks through the basics - connecting, creating accounts,
    checking balances, that sort of thing. Good starting point if you're
    new to Web3.py.
    """
    print("="*60)
    print("Ethereum Interaction with Web3.py - Stage 2")
    print("="*60 + "\n")
    
    print("Trying to connect to Ethereum...\n")
    client = EthereumClient()
    
    status = client.get_connection_status()
    print(f"Status: {json.dumps(status, indent=2)}\n")
    
    if not status.get("connected"):
        print("Looks like we can't reach the blockchain node. Let me give you some options:")
        print("1. Local: Install Ganache and run 'ganache-cli'")
        print("2. Testnet: Grab an RPC URL from Infura, Alchemy, or QuickNode")
        print("\nOnce you've got that sorted, try again.\n")
        return
    
    print("="*60)
    print("Let's create a new account")
    print("="*60 + "\n")
    
    new_account = client.create_account()
    print(f"Address: {new_account['address']}")
    print(f"Private Key: {new_account['private_key']}")
    print("\n Seriously though - never share that private key with anyone.\n")
    
    print("="*60)
    print("Checking the balance on that new account")
    print("="*60 + "\n")
    
    test_address = new_account['address']
    balance = client.get_balance(test_address)
    print(json.dumps(balance, indent=2))
    print("(Probably zero since we just made it)\n")
    
    print("="*60)
    print("Getting full account details")
    print("="*60 + "\n")
    
    account_info = client.get_account_info(test_address)
    print(json.dumps(account_info, indent=2))
    
    print("\n" + "="*60)
    print("Interactive mode - try it yourself")
    print("="*60 + "\n")
    
    while True:
        print("\nWhat do you want to do?")
        print("1. Check a balance")
        print("2. Get account details")
        print("3. Estimate gas for a transaction")
        print("4. Quit")
        
        choice = input("\nYour choice (1-4): ").strip()
        
        if choice == "1":
            address = input("Enter the address: ").strip()
            balance = client.get_balance(address)
            print(json.dumps(balance, indent=2))
        
        elif choice == "2":
            address = input("Enter the address: ").strip()
            info = client.get_account_info(address)
            print(json.dumps(info, indent=2))
        
        elif choice == "3":
            from_addr = input("Sending from: ").strip()
            to_addr = input("Sending to: ").strip()
            amount = float(input("How much ETH? (default 0.1): ").strip() or "0.1")
            
            gas_est = client.estimate_gas(from_addr, to_addr, amount)
            print(json.dumps(gas_est, indent=2))
        
        elif choice == "4":
            print("Alright, see you next time!")
            break
        
        else:
            print("Hmm, I didn't catch that. Try again?")
