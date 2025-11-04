from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from web3 import Web3
import os
from datetime import datetime
import bcrypt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///nft_marketplace.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Web3 setup
GANACHE_URL = os.getenv('GANACHE_URL', 'http://127.0.0.1:8545')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', '0x5FbDB2315678afecb367f032d93F642f64180aa3')

web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
if not web3.is_connected():
    print("Warning: Could not connect to Ganache")

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_address = db.Column(db.String(42), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class NFTMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    creator_address = db.Column(db.String(42), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_hash = db.Column(db.String(66), unique=True, nullable=False)
    token_id = db.Column(db.Integer, nullable=False)
    from_address = db.Column(db.String(42))
    to_address = db.Column(db.String(42), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # mint, transfer, sale
    price = db.Column(db.Float)  # in ETH
    block_number = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'web3_connected': web3.is_connected(),
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()

        if not data or not data.get('wallet_address') or not data.get('username') or not data.get('email'):
            return jsonify({'error': 'Missing required fields'}), 400

        # Check if user already exists
        existing_user = User.query.filter(
            (User.wallet_address == data['wallet_address']) |
            (User.username == data['username']) |
            (User.email == data['email'])
        ).first()

        if existing_user:
            return jsonify({'error': 'User already exists'}), 409

        # Create new user
        new_user = User(
            wallet_address=data['wallet_address'],
            username=data['username'],
            email=data['email']
        )

        db.session.add(new_user)
        db.session.commit()

        # Create access token
        access_token = create_access_token(identity=data['wallet_address'])

        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': {
                'wallet_address': new_user.wallet_address,
                'username': new_user.username,
                'email': new_user.email
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login with wallet address"""
    try:
        data = request.get_json()

        if not data or not data.get('wallet_address'):
            return jsonify({'error': 'Wallet address required'}), 400

        user = User.query.filter_by(wallet_address=data['wallet_address']).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        access_token = create_access_token(identity=user.wallet_address)

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'wallet_address': user.wallet_address,
                'username': user.username,
                'email': user.email
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/nfts', methods=['GET'])
def get_nfts():
    """Get all NFTs with metadata"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        nfts = NFTMetadata.query.paginate(page=page, per_page=per_page)

        result = []
        for nft in nfts.items:
            result.append({
                'token_id': nft.token_id,
                'name': nft.name,
                'description': nft.description,
                'image_url': nft.image_url,
                'creator_address': nft.creator_address,
                'created_at': nft.created_at.isoformat()
            })

        return jsonify({
            'nfts': result,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': nfts.total,
                'pages': nfts.pages
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/nfts/<int:token_id>', methods=['GET'])
def get_nft(token_id):
    """Get specific NFT metadata"""
    try:
        nft = NFTMetadata.query.filter_by(token_id=token_id).first()

        if not nft:
            return jsonify({'error': 'NFT not found'}), 404

        return jsonify({
            'token_id': nft.token_id,
            'name': nft.name,
            'description': nft.description,
            'image_url': nft.image_url,
            'creator_address': nft.creator_address,
            'created_at': nft.created_at.isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/nfts', methods=['POST'])
@jwt_required()
def create_nft_metadata():
    """Store NFT metadata (called after minting on blockchain)"""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()

        if not data or not data.get('token_id') or not data.get('name'):
            return jsonify({'error': 'Missing required fields'}), 400

        # Check if NFT already exists
        existing_nft = NFTMetadata.query.filter_by(token_id=data['token_id']).first()
        if existing_nft:
            return jsonify({'error': 'NFT metadata already exists'}), 409

        # Create NFT metadata
        new_nft = NFTMetadata(
            token_id=data['token_id'],
            name=data['name'],
            description=data.get('description', ''),
            image_url=data.get('image_url', ''),
            creator_address=current_user
        )

        db.session.add(new_nft)
        db.session.commit()

        return jsonify({
            'message': 'NFT metadata created successfully',
            'nft': {
                'token_id': new_nft.token_id,
                'name': new_nft.name,
                'description': new_nft.description,
                'image_url': new_nft.image_url,
                'creator_address': new_nft.creator_address,
                'created_at': new_nft.created_at.isoformat()
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get transaction history"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        token_id = request.args.get('token_id', type=int)

        query = Transaction.query

        if token_id:
            query = query.filter_by(token_id=token_id)

        transactions = query.order_by(Transaction.timestamp.desc()).paginate(page=page, per_page=per_page)

        result = []
        for tx in transactions.items:
            result.append({
                'transaction_hash': tx.transaction_hash,
                'token_id': tx.token_id,
                'from_address': tx.from_address,
                'to_address': tx.to_address,
                'transaction_type': tx.transaction_type,
                'price': tx.price,
                'block_number': tx.block_number,
                'timestamp': tx.timestamp.isoformat()
            })

        return jsonify({
            'transactions': result,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': transactions.total,
                'pages': transactions.pages
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/marketplace/stats', methods=['GET'])
def get_marketplace_stats():
    """Get marketplace statistics"""
    try:
        total_nfts = NFTMetadata.query.count()
        total_transactions = Transaction.query.count()
        unique_creators = db.session.query(NFTMetadata.creator_address).distinct().count()

        # Get recent sales
        recent_sales = Transaction.query.filter_by(transaction_type='sale')\
            .order_by(Transaction.timestamp.desc()).limit(5).all()

        sales_data = []
        for sale in recent_sales:
            sales_data.append({
                'token_id': sale.token_id,
                'price': sale.price,
                'timestamp': sale.timestamp.isoformat()
            })

        return jsonify({
            'total_nfts': total_nfts,
            'total_transactions': total_transactions,
            'unique_creators': unique_creators,
            'recent_sales': sales_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/<wallet_address>', methods=['GET'])
@jwt_required()
def get_user_profile(wallet_address):
    """Get user profile and their NFTs"""
    try:
        current_user = get_jwt_identity()

        # Only allow users to view their own profile or make it public
        if current_user != wallet_address:
            return jsonify({'error': 'Unauthorized'}), 403

        user = User.query.filter_by(wallet_address=wallet_address).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get user's NFTs
        user_nfts = NFTMetadata.query.filter_by(creator_address=wallet_address).all()
        nfts_data = []
        for nft in user_nfts:
            nfts_data.append({
                'token_id': nft.token_id,
                'name': nft.name,
                'description': nft.description,
                'image_url': nft.image_url,
                'created_at': nft.created_at.isoformat()
            })

        return jsonify({
            'user': {
                'wallet_address': user.wallet_address,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            },
            'nfts': nfts_data,
            'nft_count': len(nfts_data)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)