#!/usr/bin/env python3
"""
NFT Marketplace Analytics Dashboard - Backend Service
Queries Hardhat blockchain for real-time marketplace metrics
"""

import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from web3 import Web3

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Web3 connection
HARDHAT_URL = os.getenv('HARDHAT_URL', 'http://127.0.0.1:8545')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', '0x5FbDB2315678afecb367f032d93F642f64180aa3')

w3 = Web3(Web3.HTTPProvider(HARDHAT_URL))

# Load contract ABI
CONTRACT_ABI_PATH = Path('../../../stage3/nft-marketplace/smart-contracts/artifacts/contracts/NFTMarketplace.sol/NFTMarketplace.json')

def load_contract_abi():
    """Load contract ABI from compiled artifacts"""
    try:
        with open(CONTRACT_ABI_PATH, 'r') as f:
            contract_json = json.load(f)
            return contract_json['abi']
    except FileNotFoundError:
        print(f"⚠️  Contract ABI not found at {CONTRACT_ABI_PATH}")
        print("   Please compile Stage 3 contracts first:")
        print("   cd stage3/nft-marketplace/smart-contracts && npx hardhat compile")
        return None

contract_abi = load_contract_abi()
contract = None

if contract_abi and w3.is_connected():
    try:
        contract = w3.eth.contract(
            address=Web3.to_checksum_address(CONTRACT_ADDRESS),
            abi=contract_abi
        )
        print(f"✅ Connected to Hardhat: {HARDHAT_URL}")
        print(f"✅ Contract loaded: {CONTRACT_ADDRESS}")
    except Exception as e:
        print(f"⚠️  Error loading contract: {e}")
else:
    print(f"⚠️  Not connected to Hardhat or ABI not loaded")

# Cache for metrics (simple in-memory cache)
metrics_cache = {
    'last_update': None,
    'data': None
}

CACHE_DURATION = 10  # seconds

def get_marketplace_metrics():
    """Get comprehensive marketplace metrics from blockchain"""
    
    # Check cache
    if metrics_cache['last_update']:
        elapsed = (datetime.now() - metrics_cache['last_update']).seconds
        if elapsed < CACHE_DURATION and metrics_cache['data']:
            return metrics_cache['data']
    
    if not contract:
        return {
            'error': 'Contract not loaded',
            'connected': False
        }
    
    try:
        # Get current block
        current_block = w3.eth.block_number
        
        # Query past events
        from_block = max(0, current_block - 10000)  # Last 10k blocks
        
        # Get minting events
        mint_filter = contract.events.Transfer.create_filter(
            from_block=from_block,
            argument_filters={'from': '0x0000000000000000000000000000000000000000'}
        )
        mint_events = mint_filter.get_all_entries()
        
        # Get listing events  
        listing_filter = contract.events.NFTListed.create_filter(
            from_block=from_block
        )
        listing_events = listing_filter.get_all_entries()
        
        # Get sale events
        sale_filter = contract.events.NFTSold.create_filter(
            from_block=from_block
        )
        sale_events = sale_filter.get_all_entries()
        
        # Calculate metrics
        total_nfts_minted = len(mint_events)
        total_listings = len(listing_events)
        total_sales = len(sale_events)
        
        # Calculate total volume
        total_volume = sum(
            w3.from_wei(event.args.price, 'ether')
            for event in sale_events
        )
        
        # Get unique users
        unique_sellers = set(event.args.seller for event in listing_events)
        unique_buyers = set(event.args.buyer for event in sale_events)
        unique_users = len(unique_sellers | unique_buyers)
        
        # Active listings (listed but not sold)
        sold_token_ids = {event.args.tokenId for event in sale_events}
        listed_token_ids = {event.args.tokenId for event in listing_events}
        active_listings = len(listed_token_ids - sold_token_ids)
        
        # Get listing fee
        listing_fee = w3.from_wei(contract.functions.listingFee().call(), 'ether')
        
        metrics = {
            'connected': True,
            'current_block': current_block,
            'total_nfts_minted': total_nfts_minted,
            'total_listings': total_listings,
            'active_listings': active_listings,
            'total_sales': total_sales,
            'total_volume_eth': float(total_volume),
            'unique_users': unique_users,
            'listing_fee_eth': float(listing_fee),
            'avg_sale_price_eth': float(total_volume / total_sales) if total_sales > 0 else 0,
            'timestamp': datetime.now().isoformat()
        }
        
        # Update cache
        metrics_cache['data'] = metrics
        metrics_cache['last_update'] = datetime.now()
        
        return metrics
        
    except Exception as e:
        print(f"Error getting metrics: {e}")
        return {
            'error': str(e),
            'connected': False
        }

def get_recent_transactions(limit=20):
    """Get recent marketplace transactions"""
    if not contract:
        return []
    
    try:
        current_block = w3.eth.block_number
        from_block = max(0, current_block - 10000)
        
        # Get all events
        mint_events = contract.events.Transfer.create_filter(
            from_block=from_block,
            argument_filters={'from': '0x0000000000000000000000000000000000000000'}
        ).get_all_entries()
        
        listing_events = contract.events.NFTListed.create_filter(
            from_block=from_block
        ).get_all_entries()
        
        sale_events = contract.events.NFTSold.create_filter(
            from_block=from_block
        ).get_all_entries()
        
        # Format transactions
        transactions = []
        
        for event in mint_events[-limit:]:
            transactions.append({
                'type': 'mint',
                'token_id': event.args.tokenId,
                'address': event.args.to,
                'block': event.blockNumber,
                'tx_hash': event.transactionHash.hex()
            })
        
        for event in listing_events[-limit:]:
            transactions.append({
                'type': 'list',
                'token_id': event.args.tokenId,
                'seller': event.args.seller,
                'price_eth': float(w3.from_wei(event.args.price, 'ether')),
                'block': event.blockNumber,
                'tx_hash': event.transactionHash.hex()
            })
        
        for event in sale_events[-limit:]:
            transactions.append({
                'type': 'sale',
                'token_id': event.args.tokenId,
                'buyer': event.args.buyer,
                'seller': event.args.seller,
                'price_eth': float(w3.from_wei(event.args.price, 'ether')),
                'block': event.blockNumber,
                'tx_hash': event.transactionHash.hex()
            })
        
        # Sort by block number (most recent first)
        transactions.sort(key=lambda x: x['block'], reverse=True)
        
        return transactions[:limit]
        
    except Exception as e:
        print(f"Error getting transactions: {e}")
        return []

# REST API Endpoints

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'connected': w3.is_connected() if w3 else False,
        'contract_loaded': contract is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/metrics', methods=['GET'])
def metrics():
    """Get marketplace metrics"""
    return jsonify(get_marketplace_metrics())

@app.route('/api/transactions', methods=['GET'])
def transactions():
    """Get recent transactions"""
    limit = request.args.get('limit', default=20, type=int)
    return jsonify({
        'transactions': get_recent_transactions(limit),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/stats/daily', methods=['GET'])
def daily_stats():
    """Get daily statistics"""
    # TODO: Implement daily aggregation
    return jsonify({
        'message': 'Daily stats endpoint - to be implemented',
        'data': []
    })

# WebSocket Events

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('connection_status', {'status': 'connected'})
    
    # Send initial metrics
    emit('metrics_update', get_marketplace_metrics())

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('request_metrics')
def handle_metrics_request():
    """Handle metrics request from client"""
    emit('metrics_update', get_marketplace_metrics())

@socketio.on('request_transactions')
def handle_transactions_request(data):
    """Handle transactions request from client"""
    limit = data.get('limit', 20)
    emit('transactions_update', {
        'transactions': get_recent_transactions(limit)
    })

# Background task for real-time updates
def background_metrics_update():
    """Continuously send metrics updates to connected clients"""
    import time
    while True:
        time.sleep(5)  # Update every 5 seconds
        metrics = get_marketplace_metrics()
        socketio.emit('metrics_update', metrics, broadcast=True)

if __name__ == '__main__':
    print("\n" + "="*60)
    print(" NFT Marketplace Analytics Dashboard - Backend ".center(60, "="))
    print("="*60)
    print(f"\n📊 Starting analytics service...")
    print(f"   Hardhat URL: {HARDHAT_URL}")
    print(f"   Contract: {CONTRACT_ADDRESS}")
    print(f"\n🌐 Server will run on: http://localhost:{os.getenv('PORT', 5001)}")
    print(f"   API Docs: http://localhost:{os.getenv('PORT', 5001)}/api/health")
    print("\n" + "="*60 + "\n")
    
    # Start background task
    # socketio.start_background_task(background_metrics_update)
    
    # Run server
    socketio.run(
        app,
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5001)),
        debug=True,
        allow_unsafe_werkzeug=True
    )
