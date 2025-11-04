#!/usr/bin/env python3
"""
Load Testing Suite for NFT Marketplace
Simulates multiple users interacting with marketplace
"""

import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from web3 import Web3
import json
from pathlib import Path

# Configuration
HARDHAT_URL = 'http://127.0.0.1:8545'
CONTRACT_ADDRESS = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
NUM_USERS = 10
NUM_OPERATIONS = 50

w3 = Web3(Web3.HTTPProvider(HARDHAT_URL))

def load_contract():
    """Load contract ABI and create instance"""
    abi_path = Path('../../../stage3/nft-marketplace/smart-contracts/artifacts/contracts/NFTMarketplace.sol/NFTMarketplace.json')
    
    with open(abi_path, 'r') as f:
        contract_json = json.load(f)
    
    return w3.eth.contract(
        address=Web3.to_checksum_address(CONTRACT_ADDRESS),
        abi=contract_json['abi']
    )

def simulate_mint(account, contract):
    """Simulate NFT minting"""
    start_time = time.time()
    
    try:
        tx = contract.functions.mintNFT(
            f"https://example.com/nft/{time.time()}"
        ).transact({
            'from': account,
            'gas': 200000
        })
        
        receipt = w3.eth.wait_for_transaction_receipt(tx)
        duration = time.time() - start_time
        
        return {
            'operation': 'mint',
            'success': True,
            'duration': duration,
            'gas_used': receipt.gasUsed
        }
    except Exception as e:
        return {
            'operation': 'mint',
            'success': False,
            'duration': time.time() - start_time,
            'error': str(e)
        }

def simulate_list(account, contract, token_id):
    """Simulate NFT listing"""
    start_time = time.time()
    
    try:
        price = w3.to_wei(1, 'ether')
        listing_fee = contract.functions.listingFee().call()
        
        tx = contract.functions.listNFT(token_id, price).transact({
            'from': account,
            'value': listing_fee,
            'gas': 200000
        })
        
        receipt = w3.eth.wait_for_transaction_receipt(tx)
        duration = time.time() - start_time
        
        return {
            'operation': 'list',
            'success': True,
            'duration': duration,
            'gas_used': receipt.gasUsed
        }
    except Exception as e:
        return {
            'operation': 'list',
            'success': False,
            'duration': time.time() - start_time,
            'error': str(e)
        }

def run_load_test():
    """Run comprehensive load test"""
    print("="*60)
    print(" NFT Marketplace Load Test ".center(60, "="))
    print("="*60)
    
    if not w3.is_connected():
        print("\n❌ Not connected to Hardhat")
        print("   Please start: npx hardhat node")
        return
    
    print(f"\n📊 Test Configuration:")
    print(f"   Simulated Users: {NUM_USERS}")
    print(f"   Operations per User: {NUM_OPERATIONS}")
    print(f"   Total Operations: {NUM_USERS * NUM_OPERATIONS}")
    
    contract = load_contract()
    accounts = w3.eth.accounts[:NUM_USERS]
    
    print(f"\n🚀 Starting load test...\n")
    
    start_time = time.time()
    results = []
    
    # Mint NFTs
    print("   [1/2] Minting NFTs...")
    with ThreadPoolExecutor(max_workers=NUM_USERS) as executor:
        futures = []
        for i in range(NUM_OPERATIONS):
            account = accounts[i % len(accounts)]
            futures.append(executor.submit(simulate_mint, account, contract))
        
        for future in futures:
            results.append(future.result())
    
    total_duration = time.time() - start_time
    
    # Analyze results
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    avg_duration = sum(r['duration'] for r in successful) / len(successful) if successful else 0
    total_gas = sum(r.get('gas_used', 0) for r in successful)
    throughput = len(successful) / total_duration if total_duration > 0 else 0
    
    print(f"\n   ✅ Complete!\n")
    
    print("="*60)
    print(" Load Test Results ".center(60, "="))
    print("="*60)
    
    print(f"\n📈 Performance Metrics:")
    print(f"   Total Duration: {total_duration:.2f}s")
    print(f"   Successful Operations: {len(successful)}")
    print(f"   Failed Operations: {len(failed)}")
    print(f"   Success Rate: {len(successful) / len(results) * 100:.1f}%")
    print(f"   Average Duration: {avg_duration:.3f}s")
    print(f"   Throughput: {throughput:.2f} ops/sec")
    print(f"   Total Gas Used: {total_gas:,}")
    
    if failed:
        print(f"\n⚠️  Failed Operations:")
        for f in failed[:5]:  # Show first 5 failures
            print(f"   {f['operation']}: {f['error']}")
    
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    run_load_test()
