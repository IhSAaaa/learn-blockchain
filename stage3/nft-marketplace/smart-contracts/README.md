# NFT Marketplace Smart Contracts

This directory contains the Solidity smart contracts for the NFT Marketplace dApp built with Hardhat.

## Features

- **ERC-721 NFT Standard**: Full ERC-721 compliance with URI storage
- **Marketplace Functionality**: List, buy, and cancel NFT listings
- **Platform Fees**: Configurable listing fees collected by contract owner
- **Secure Payments**: Funds held in escrow until withdrawal
- **Reentrancy Protection**: Built-in protection against reentrancy attacks
- **Access Control**: Owner-only administrative functions

## Contract Overview

### NFTMarketplace.sol

Main contract that combines:
- ERC-721 token functionality
- Marketplace listing and purchasing
- Fee collection and management
- Secure fund withdrawals

#### Key Functions

- `mintNFT(string tokenURI)`: Mint new NFT with metadata URI
- `listNFT(uint256 tokenId, uint256 price)`: List NFT for sale (requires listing fee)
- `buyNFT(uint256 tokenId)`: Purchase listed NFT
- `cancelListing(uint256 tokenId)`: Cancel active listing
- `withdrawFunds()`: Withdraw accumulated sale proceeds
- `setListingFee(uint256 newFee)`: Update listing fee (owner only)

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

3. Fill in your environment variables:
- `PRIVATE_KEY`: Your wallet private key (never commit!)
- `SEPOLIA_RPC_URL`: Sepolia testnet RPC endpoint
- `ETHERSCAN_API_KEY`: For contract verification

## Usage

### Local Development

1. Start local Hardhat network:
```bash
npx hardhat node
```

2. Deploy contracts:
```bash
npm run deploy
```

3. Run tests:
```bash
npm test
```

### Testnet Deployment

1. Deploy to Sepolia:
```bash
npm run deploy:sepolia
```

2. Verify contract:
```bash
npm run verify
```

## Testing

Run the comprehensive test suite:
```bash
npm test
```

Run tests with gas reporting:
```bash
npm run test:gas
```

## Code Quality

Lint Solidity code:
```bash
npm run lint
```

Auto-fix linting issues:
```bash
npm run lint:fix
```

## Security Considerations

- ReentrancyGuard protects against reentrancy attacks
- Funds are held in escrow until explicit withdrawal
- Listing fees prevent spam listings
- Automatic listing cancellation on transfer prevents invalid sales
- Input validation on all public functions

## Gas Optimization

- Uses Solidity 0.8.20 with optimizer enabled (200 runs)
- Efficient storage patterns
- Minimal external calls
- Gas reporting available for optimization analysis