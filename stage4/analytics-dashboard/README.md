# Analytics Dashboard

Build comprehensive on-chain analytics for the NFT marketplace running on local blockchain.

## Overview

Real-time analytics dashboard featuring:
- Marketplace statistics (all from local Hardhat blockchain)
- Trading volume metrics
- Popular NFTs and creators
- Price trends and history
- User activity insights

## Tech Stack

**Backend (Python)**
- Flask API
- Pandas for data analysis
- Web3.py for local blockchain queries
- SQLite for local caching

**Frontend (React)**
- React with Chart.js or Recharts
- Real-time data updates via WebSocket
- Interactive visualizations
- Responsive design

## Architecture

```
Local Hardhat Node (Port 8545)
    ↓
Flask Backend (Port 5000)
    - Queries local blockchain
    - Processes data with Pandas
    - Caches in SQLite
    ↓
React Frontend (Port 3000)
    - Displays charts and metrics
    - Real-time updates
    - Interactive dashboard
```

## Features

### 1. Marketplace Metrics
- Total NFTs minted
- Active listings count
- Total sales volume
- Platform fees collected
- Average sale price

### 2. Trading Analytics
- Daily/Weekly/Monthly volume
- Average sale price trends
- Price distribution
- Sales by category
- Most active time periods

### 3. User Analytics
- Top creators by volume
- Top buyers
- User activity timeline
- Wallet distribution
- New users per day

### 4. NFT Analytics
- Trending NFTs (most viewed/bought)
- Recently minted
- Price history for each NFT
- Most expensive listings
- Most active sellers

## Getting Started

### 1. Setup Backend

```bash
cd analytics-dashboard/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Update .env with local Hardhat info
# WEB3_PROVIDER_URL=http://127.0.0.1:8545
# CONTRACT_ADDRESS=0x... (from Stage 3 deployment)
```

### 2. Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start frontend
npm start
```

### 3. Run Local Blockchain

```bash
# In a separate terminal
cd stage3/nft-marketplace/smart-contracts
npx hardhat node
```

### 4. Start Backend

```bash
cd stage4/analytics-dashboard/backend

# Activate venv
source venv/bin/activate

# Run Flask app
python app.py
```

## API Endpoints

```
GET /api/stats/overview       # Overall marketplace stats
GET /api/stats/volume         # Trading volume data
GET /api/stats/trending       # Trending NFTs
GET /api/nfts/recent          # Recently minted NFTs
GET /api/nfts/<token_id>      # Single NFT details
GET /api/users/top-creators   # Top creators
GET /api/users/top-buyers     # Top buyers
GET /api/market/prices        # Price history
```

## Data Collection

The backend automatically:
1. Listens to local blockchain events
2. Queries smart contract state
3. Processes and aggregates data
4. Stores in SQLite cache
5. Serves via REST API

## Database Schema

```sql
-- NFTs
CREATE TABLE nfts (
  token_id INTEGER PRIMARY KEY,
  creator TEXT,
  name TEXT,
  description TEXT,
  listed BOOLEAN,
  price DECIMAL,
  created_at TIMESTAMP
);

-- Transactions
CREATE TABLE transactions (
  id INTEGER PRIMARY KEY,
  token_id INTEGER,
  from_address TEXT,
  to_address TEXT,
  price DECIMAL,
  tx_hash TEXT,
  timestamp TIMESTAMP
);

-- Listings
CREATE TABLE listings (
  id INTEGER PRIMARY KEY,
  token_id INTEGER,
  seller TEXT,
  price DECIMAL,
  active BOOLEAN,
  created_at TIMESTAMP
);
```

## Dashboard Views

1. **Overview Dashboard**
   - Key metrics cards
   - Total volume chart
   - Active listings count

2. **Trading Analytics**
   - Volume over time
   - Price distribution
   - Most traded NFTs

3. **User Analytics**
   - Top creators
   - Top buyers
   - User activity heatmap

4. **NFT Details**
   - Individual NFT info
   - Price history
   - Buyer/seller timeline

## Real-time Updates

The frontend uses WebSocket to receive real-time updates:
```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:5000/ws/updates');

// Receive live events
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateDashboard(data);
};
```

## Performance Considerations

- Cache frequently accessed data in SQLite
- Use pagination for large datasets
- Batch process blockchain queries
- Optimize React re-renders with memoization

## Development Workflow

```bash
# Terminal 1: Hardhat node
npx hardhat node

# Terminal 2: Flask backend
cd stage4/analytics-dashboard/backend
python app.py

# Terminal 3: React frontend
cd stage4/analytics-dashboard/frontend
npm start

# Terminal 4: Manually test marketplace
cd stage3/nft-marketplace/frontend
npm start
```

## Metrics to Track

- Total NFTs minted
- Active listings
- Total trading volume
- Number of users
- Average transaction size
- Peak transaction times

## Status

🚧 **Coming Soon** - Will be built after gas optimization phase.

## Next Steps

1. Implement backend Flask API
2. Create SQLite schema
3. Build React dashboard components
4. Add real-time WebSocket updates
5. Deploy analytics to production environment

