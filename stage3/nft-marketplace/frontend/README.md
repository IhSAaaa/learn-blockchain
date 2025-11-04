# NFT Marketplace Frontend

A modern React-based frontend for the NFT Marketplace dApp, featuring wallet integration, NFT browsing, and marketplace functionality.

## Features

- **Wallet Integration**: MetaMask connection with automatic network switching
- **NFT Marketplace**: Browse and purchase listed NFTs
- **NFT Management**: View your collection, list NFTs for sale, and manage listings
- **NFT Creation**: Mint new NFTs with custom metadata
- **Responsive Design**: Bootstrap-based UI that works on all devices
- **Real-time Updates**: Live updates of NFT listings and ownership

## Tech Stack

- **React 18**: Modern React with hooks and functional components
- **Web3.js**: Ethereum blockchain interaction
- **React Router**: Client-side routing
- **Bootstrap 5**: Responsive UI components
- **React Bootstrap**: Bootstrap components for React

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Add your contract address to `.env`:
```
REACT_APP_CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3
```

4. Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## Project Structure

```
src/
├── components/          # Reusable UI components
│   └── Header.js       # Navigation header with wallet connection
├── context/            # React context for global state
│   └── Web3Context.js  # Web3 and wallet management
├── contracts/          # Smart contract ABIs
│   └── NFTMarketplace.json
├── pages/              # Main application pages
│   ├── Home.js         # Landing page with overview
│   ├── Marketplace.js  # NFT browsing and purchasing
│   ├── MyNFTs.js       # User's NFT collection management
│   └── CreateNFT.js    # NFT minting interface
├── App.js              # Main app component with routing
├── App.css             # Global styles
└── index.js            # App entry point
```

## Key Components

### Web3Context
Manages all blockchain interactions:
- Wallet connection/disconnection
- Network switching
- Contract initialization
- Error handling

### Pages

- **Home**: Welcome page with feature overview and getting started guide
- **Marketplace**: Grid view of listed NFTs with purchase functionality
- **MyNFTs**: User's NFT collection with listing management
- **CreateNFT**: Form for minting new NFTs with metadata

## Smart Contract Integration

The frontend interacts with the NFTMarketplace smart contract for:
- Reading NFT listings and metadata
- Purchasing NFTs (via MetaMask)
- Listing NFTs for sale
- Minting new NFTs
- Managing user funds

## Development Notes

- Uses dual Web3 provider pattern: Ganache for reads, MetaMask for writes
- Implements proper error handling and loading states
- Responsive design works on mobile and desktop
- Gas estimation and transaction handling included

## Environment Variables

- `REACT_APP_CONTRACT_ADDRESS`: Deployed contract address (required)

## Available Scripts

- `npm start`: Start development server
- `npm run build`: Create production build
- `npm test`: Run tests
- `npm run eject`: Eject from Create React App

## Browser Support

- Modern browsers with MetaMask extension
- Chrome, Firefox, Safari, Edge
- Mobile browsers (limited MetaMask support)