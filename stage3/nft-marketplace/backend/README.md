# NFT Marketplace Backend API

A Flask-based REST API for the NFT Marketplace dApp, providing user management, NFT metadata storage, and marketplace analytics.

## Features

- **User Management**: Registration and authentication with wallet addresses
- **NFT Metadata Storage**: Off-chain storage of NFT metadata and attributes
- **Transaction History**: Complete transaction logging and analytics
- **Marketplace Analytics**: Statistics and insights for the marketplace
- **JWT Authentication**: Secure API endpoints with JSON Web Tokens
- **CORS Support**: Cross-origin requests for frontend integration

## Tech Stack

- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **Flask-JWT-Extended**: JWT token management
- **Web3.py**: Ethereum blockchain interaction
- **Flask-CORS**: Cross-origin resource sharing

## Getting Started

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
python -c "from app import db; db.create_all()"
```

5. Run the development server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login with wallet address

### NFTs
- `GET /api/nfts` - Get all NFTs (paginated)
- `GET /api/nfts/<token_id>` - Get specific NFT
- `POST /api/nfts` - Create NFT metadata (requires auth)

### Transactions
- `GET /api/transactions` - Get transaction history

### Analytics
- `GET /api/marketplace/stats` - Get marketplace statistics

### User
- `GET /api/user/<wallet_address>` - Get user profile (requires auth)

### Health
- `GET /api/health` - Health check endpoint

## Database Schema

### User
- `id`: Primary key
- `wallet_address`: Ethereum wallet address (unique)
- `username`: Display name (unique)
- `email`: Email address (unique)
- `created_at`: Registration timestamp

### NFTMetadata
- `id`: Primary key
- `token_id`: Blockchain token ID (unique)
- `name`: NFT name
- `description`: NFT description
- `image_url`: Image URL
- `creator_address`: Creator's wallet address
- `created_at`: Creation timestamp

### Transaction
- `id`: Primary key
- `transaction_hash`: Blockchain transaction hash (unique)
- `token_id`: NFT token ID
- `from_address`: Sender address
- `to_address`: Receiver address
- `transaction_type`: Type (mint, transfer, sale)
- `price`: Transaction price in ETH
- `block_number`: Blockchain block number
- `timestamp`: Transaction timestamp

## Environment Variables

- `SECRET_KEY`: Flask secret key
- `JWT_SECRET_KEY`: JWT signing key
- `DATABASE_URL`: Database connection string
- `GANACHE_URL`: Ganache RPC endpoint
- `CONTRACT_ADDRESS`: Deployed contract address

## Development

### Running Tests
```bash
# Add test commands here when implemented
```

### Database Migrations
```bash
# For production, consider using Flask-Migrate
# flask db init
# flask db migrate
# flask db upgrade
```

### API Documentation
Access the API documentation at `/api/docs` (if Swagger is implemented)

## Security Considerations

- JWT tokens for API authentication
- Input validation on all endpoints
- CORS configuration for frontend integration
- Environment variables for sensitive data
- SQL injection prevention with SQLAlchemy

## Deployment

### Local Development
```bash
python app.py
```

### Production
Consider using:
- Gunicorn as WSGI server
- PostgreSQL for database
- Redis for session storage
- Nginx as reverse proxy

Example with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Integration with Frontend

The backend is designed to work with the React frontend:

1. User registration/login through wallet connection
2. NFT metadata storage after minting
3. Transaction history and analytics
4. User profile management

## Future Enhancements

- IPFS integration for decentralized metadata storage
- WebSocket support for real-time updates
- Advanced analytics and reporting
- NFT rarity calculations
- Auction functionality
- Social features (likes, comments)