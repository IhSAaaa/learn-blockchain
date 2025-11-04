# Stage 3: Build DApps - NFT Marketplace

A complete NFT marketplace dApp built with modern web technologies, featuring smart contracts, React frontend, and Flask backend API.

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  Flask Backend  │    │ Smart Contracts │
│                 │    │                 │    │                 │
│ - Wallet Connect│◄──►│ - User Management│◄──►│ - NFT Creation │
│ - NFT Browsing  │    │ - NFT Metadata   │    │ - Marketplace   │
│ - Marketplace   │    │ - Analytics      │    │ - Escrow       │
│ - User Dashboard│    │ - API Endpoints  │    │ - Royalties     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │     Ganache     │
                    │   Test Network  │
                    └─────────────────┘
```

## Features

### Smart Contracts (Hardhat + Solidity)
- **ERC-721 NFT Standard**: Full NFT implementation with metadata
- **Marketplace Functionality**: List, buy, and cancel NFT sales
- **Platform Fees**: Configurable listing fees for platform sustainability
- **Secure Escrow**: Funds held safely until transaction completion
- **Reentrancy Protection**: Built-in security against common attacks

### Frontend (React + Web3.js)
- **Wallet Integration**: MetaMask connection with network switching
- **NFT Marketplace**: Browse and purchase NFTs with real-time updates
- **NFT Management**: View collection, list items, manage earnings
- **NFT Creation**: Mint new NFTs with custom metadata
- **Responsive Design**: Works seamlessly on desktop and mobile

### Backend (Flask + SQLAlchemy)
- **User Management**: Registration and authentication system
- **NFT Metadata Storage**: Off-chain metadata with blockchain verification
- **Transaction History**: Complete audit trail of all marketplace activity
- **Analytics Dashboard**: Marketplace statistics and insights
- **RESTful API**: Well-documented endpoints for frontend integration

## Tech Stack

- **Blockchain**: Solidity, Hardhat, OpenZeppelin, Web3.js
- **Frontend**: React 18, React Router, Bootstrap 5, Web3.js
- **Backend**: Flask, SQLAlchemy, JWT, Flask-CORS
- **Database**: SQLite (development), PostgreSQL (production)
- **Testing**: Hardhat (contracts), Jest (frontend), pytest (backend)
- **Development**: Ganache, MetaMask, Node.js, Python

## Prerequisites

- **Node.js** (v16+)
- **Python** (v3.8+)
- **Ganache** (local Ethereum network)
- **MetaMask** (browser wallet)
- **Git**

## Quick Start

### 1. Clone and Setup
```bash
cd stage3/nft-marketplace
```

### 2. Smart Contracts Setup
```bash
cd smart-contracts
npm install
cp .env.example .env
# Edit .env with your configuration
npm run compile
npm run test
npx hardhat node  # Start local network
npm run deploy   # Deploy contracts
```

### 3. Backend Setup
```bash
cd ../backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with contract address
python app.py
```

### 4. Frontend Setup
```bash
cd ../frontend
npm install
cp .env.example .env
# Add contract address to .env
npm start
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Smart Contracts**: Deployed to local Ganache network

## 📁 Project Structure

```
stage3/nft-marketplace/
├── smart-contracts/          # Hardhat project
│   ├── contracts/           # Solidity contracts
│   ├── scripts/            # Deployment scripts
│   ├── test/               # Contract tests
│   └── hardhat.config.js   # Hardhat configuration
├── frontend/                # React application
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── context/        # React context
│   │   ├── pages/          # Application pages
│   │   └── contracts/      # Contract ABIs
│   └── package.json
├── backend/                 # Flask API
│   ├── app.py              # Main application
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Backend documentation
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

#### Smart Contracts (.env)
```
PRIVATE_KEY=your_private_key
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
ETHERSCAN_API_KEY=your_etherscan_api_key
```

#### Backend (.env)
```
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URL=sqlite:///nft_marketplace.db
GANACHE_URL=http://127.0.0.1:8545
CONTRACT_ADDRESS=deployed_contract_address
```

#### Frontend (.env)
```
REACT_APP_CONTRACT_ADDRESS=deployed_contract_address
```

## 🧪 Testing

### Smart Contracts
```bash
cd smart-contracts
npm test
npm run test:gas  # With gas reporting
```

### Frontend
```bash
cd frontend
npm test
```

### Backend
```bash
cd backend
# Add pytest configuration and tests
```

## 🚢 Deployment

### Local Development
1. Start Ganache: `npx hardhat node`
2. Deploy contracts: `npm run deploy`
3. Start backend: `python app.py`
4. Start frontend: `npm start`

### Testnet Deployment
1. Update network configuration in `hardhat.config.js`
2. Deploy to Sepolia: `npm run deploy:sepolia`
3. Update contract addresses in frontend/backend
4. Build frontend: `npm run build`
5. Deploy frontend to Vercel/Netlify

## Security Features

- **Reentrancy Protection**: OpenZeppelin ReentrancyGuard
- **Access Control**: Owner-only administrative functions
- **Input Validation**: Comprehensive validation on all inputs
- **JWT Authentication**: Secure API access
- **CORS Configuration**: Controlled cross-origin access

## API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### NFT Endpoints
- `GET /api/nfts` - List NFTs
- `POST /api/nfts` - Create NFT metadata
- `GET /api/nfts/{token_id}` - Get NFT details

### Marketplace Endpoints
- `GET /api/marketplace/stats` - Marketplace statistics
- `GET /api/transactions` - Transaction history

## Learning Objectives Achieved

- **Solidity Development**: Advanced smart contract patterns
- **Web3 Integration**: Frontend blockchain interaction
- **Full-Stack Development**: React + Flask + Blockchain
- **Security Best Practices**: Reentrancy protection, access control
- **Testing**: Comprehensive test coverage
- **Deployment**: Multi-environment deployment strategies

## Next Steps

- **IPFS Integration**: Decentralized metadata storage
- **Layer 2 Scaling**: Polygon/ZK-rollup integration
- **Cross-chain Bridge**: Multi-chain NFT trading
- **Advanced Features**: Auctions, royalties, collections
- **Mobile App**: React Native implementation

## Resources

- [Hardhat Documentation](https://hardhat.org/)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)
- [Web3.js Documentation](https://web3js.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [ERC-721 Standard](https://eips.ethereum.org/EIPS/eip-721)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is part of the Blockchain Engineer learning path. See the main project license for details.