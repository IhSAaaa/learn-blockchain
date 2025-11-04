# Stage 4: Local Optimization & Analytics - Getting Started

Welcome to Stage 4! You've completed the blockchain simulation, smart contracts, and full-stack dApp. Now let's optimize performance and build powerful analytics on your local Hardhat network.

## Prerequisites

Before starting Stage 4, verify you have:

```bash
# Stage 3 fully operational
cd stage3/nft-marketplace

# 1. Hardhat running
npx hardhat node  # Should output "Started HTTP and WebSocket JSON-RPC server at http://127.0.0.1:8545"

# 2. Contracts deployed (in another terminal)
npm run deploy  # Should complete without errors

# 3. Flask backend running
cd stage3/nft-marketplace/backend
python app.py  # Should show "Running on http://127.0.0.1:5000"

# 4. React frontend running
cd stage3/nft-marketplace/frontend
npm start  # Should open http://localhost:3000
```

✅ If all 4 are running → You're ready for Stage 4!

## Stage 4 Overview

Stage 4 focuses on **local optimization and analytics** for your NFT marketplace. No external services, no testnet deployments—everything runs on your local Hardhat network.

### Three Phases (Local-Only)

| Phase | Focus | Output |
|-------|-------|--------|
| **Phase 1** | Gas Optimization | Gas report, optimized contracts |
| **Phase 2** | Analytics Dashboard | Performance metrics, real-time updates |
| **Phase 3** | Performance Monitoring | Benchmarks, load tests, optimization guide |

## Phase 1: Gas Optimization (Start Here!)

**Goal**: Analyze and optimize smart contract gas usage on Hardhat.

### Quick Start

```bash
cd stage4/gas-optimization
cat README.md  # Read full details
```

### What You'll Do

1. **Generate Gas Report**
   ```bash
   cd stage3/nft-marketplace/smart-contracts
   REPORT_GAS=true npm test
   ```
   Creates `gas-report.txt` with breakdown per function.

2. **Analyze Results**
   - Identify expensive operations (mint, listing, purchase)
   - Find optimization opportunities
   - Prioritize high-impact changes

3. **Implement Optimizations**
   - Batch operations
   - Optimize storage access
   - Reduce redundant calculations
   - Apply Solidity best practices

4. **Verify Improvements**
   - Re-run gas report
   - Compare before/after
   - Document gas savings (%)

### Success Criteria

✅ Gas report generated
✅ Top 3 expensive functions identified
✅ At least 2 optimization techniques implemented
✅ 5-15% gas reduction achieved
✅ All tests still passing (22/22)

### Estimated Time: 2-3 hours

## Phase 2: Analytics Dashboard (After Phase 1)

**Goal**: Build a dashboard to visualize marketplace metrics from local Hardhat.

### Quick Start

```bash
cd stage4/analytics-dashboard
cat README.md  # Read full details
```

### What You'll Build

1. **Backend Metrics API** (Flask)
   - Query Hardhat blockchain for marketplace data
   - Track NFT supply, listings, sales volume
   - Monitor user activity and transaction patterns
   - Cache data in SQLite for performance

2. **Frontend Dashboard** (React)
   - Real-time marketplace metrics
   - Historical trends and charts
   - User activity visualization
   - Transaction history with filters

3. **WebSocket Updates**
   - Live updates when new transactions occur
   - Real-time listener for blockchain events
   - Bi-directional communication

### Success Criteria

✅ Dashboard displays live marketplace data
✅ Charts show historical trends (NFTs minted, sales)
✅ Real-time updates via WebSocket
✅ Performance metrics visible
✅ Mobile-responsive design

### Estimated Time: 3-4 hours

## Phase 3: Performance Monitoring (Final Phase)

**Goal**: Benchmark system performance and identify optimization opportunities.

### Quick Start

```bash
cd stage4/performance-monitoring
cat README.md  # Read full details
```

### What You'll Build

1. **Performance Monitoring Service**
   - Track API response times
   - Monitor contract execution times
   - Measure database query performance
   - Collect system metrics (CPU, memory)

2. **Benchmarking Suite**
   - Load testing (simulate 100+ users)
   - Stress testing (push to limits)
   - Throughput measurement
   - Baseline establishment

3. **Performance Dashboard**
   - View real-time metrics
   - Historical performance trends
   - Bottleneck identification
   - Optimization recommendations

### Success Criteria

✅ Monitoring service running
✅ Performance baseline established
✅ Load test results documented
✅ Bottlenecks identified
✅ Optimization recommendations generated

### Estimated Time: 2-3 hours

## Architecture (Local-Only)

```
┌────────────────────────────────────────────────────────┐
│                    Your Machine                         │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Hardhat Local Network (Port 8545)                     │
│  ├─ NFTMarketplace.sol                                 │
│  └─ 22 test cases (all passing)                        │
│                                                         │
│  Flask Backend (Port 5000)                             │
│  ├─ /api/nfts (query blockchain)                       │
│  ├─ /api/analytics (compute metrics)                   │
│  └─ /api/users (user management)                       │
│                                                         │
│  React Frontend (Port 3000)                            │
│  ├─ Marketplace UI                                     │
│  ├─ Analytics Dashboard                                │
│  └─ Performance Monitor                                │
│                                                         │
│  SQLite Database (stage3/backend/)                     │
│  └─ Metrics cache, user data                           │
│                                                         │
└────────────────────────────────────────────────────────┘
```

**Key Points:**
- ✅ All components run locally
- ✅ No external services needed
- ✅ No testnet transactions required
- ✅ No deployment costs
- ✅ Fast iteration and testing

## Common Workflow

### Every Session

```bash
# Terminal 1: Hardhat (always first!)
cd stage3/nft-marketplace/smart-contracts
npx hardhat node

# Terminal 2: Flask backend
cd stage3/nft-marketplace/backend
source venv/bin/activate
python app.py

# Terminal 3: React frontend (optional for Phase 1)
cd stage3/nft-marketplace/frontend
npm start

# Terminal 4: Stage 4 work
cd stage4/<phase>
# Run current phase tasks
```

### Before Each Phase

```bash
# Ensure Stage 3 is still running
curl http://localhost:5000/api/users  # Should work
curl http://localhost:8545 -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"eth_blockNumber","id":1}' # Should work
```

## Tips & Tricks

### 1. Keep Hardhat Running
- Don't close Terminal 1 (Hardhat)
- If closed, all local data is lost
- Just restart and re-deploy

### 2. Fresh Start
```bash
# Clear all local data and restart
cd stage3/nft-marketplace/smart-contracts
npx hardhat clean
npx hardhat node  # Fresh network
```

### 3. Test as You Go
```bash
# Before each optimization
npm run test  # All 22 tests must pass
REPORT_GAS=true npm test  # Check gas impact
```

### 4. Document Everything
- Record initial gas metrics
- Note optimization techniques used
- Compare before/after results
- Explain performance improvements

## Project Structure

```
stage4/
├── README.md                      # Stage 4 overview
├── GETTING-STARTED.md             # This file
├── gas-optimization/
│   ├── README.md                  # Phase 1 details
│   ├── requirements.txt            # Python dependencies
│   └── scripts/
│       ├── analyze-gas.py         # Gas analysis tool
│       └── optimize.py            # Optimization helper
├── analytics-dashboard/
│   ├── README.md                  # Phase 2 details
│   ├── requirements.txt            # Python dependencies
│   └── src/
│       ├── dashboard.py           # Flask analytics API
│       └── components/            # React components
└── performance-monitoring/
    ├── README.md                  # Phase 3 details
    ├── requirements.txt            # Python dependencies
    └── monitor.py                 # Monitoring service
```

## Resources

### Documentation
- [Hardhat Documentation](https://hardhat.org/docs)
- [Solidity Gas Optimization](https://docs.soliditylang.org/en/latest/gas-optimization.html)
- [Web3.py](https://web3py.readthedocs.io/)
- [React Documentation](https://react.dev/)

### Tools
- **Gas Analysis**: Hardhat gas-reporter plugin
- **Performance**: Prometheus + Grafana
- **Testing**: Hardhat + Chai + ethers.js

## Troubleshooting

### "Hardhat port 8545 already in use"
```bash
# Find and kill process
lsof -i :8545
kill -9 <PID>
# Or use different port
npx hardhat node --port 8546
```

### "Contract not deployed"
```bash
# Ensure Hardhat is running first, then:
cd stage3/nft-marketplace/smart-contracts
npm run deploy
```

### "Flask can't connect to blockchain"
```bash
# Verify Hardhat is running
curl http://localhost:8545 -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"eth_blockNumber","id":1}'
# Should return: {"jsonrpc":"2.0","result":"0x...","id":1}
```

### "React dashboard not showing data"
```bash
# Check Flask is running
curl http://localhost:5000/api/nfts
# Should return JSON with NFT data
```

## Success Checklist

By end of Stage 4, you will have:

- ✅ **Phase 1**: Analyzed gas usage, optimized contracts, documented savings
- ✅ **Phase 2**: Built real-time analytics dashboard with charts
- ✅ **Phase 3**: Benchmarked performance, identified bottlenecks
- ✅ **Documentation**: Complete optimization guide with before/after metrics
- ✅ **Understanding**: Deep knowledge of blockchain performance tuning

## Next Steps After Stage 4

After completing all three phases:
- 📚 Study additional Solidity optimization techniques
- 🔬 Experiment with different data structures
- 📊 Build custom analytics for your own metrics
- 🚀 Consider testnet deployment (when budget allows)
- 💡 Design your own blockchain features

## Questions?

Refer to:
1. Individual phase README files
2. `.github/copilot-instructions.md` (comprehensive reference)
3. Stage 3 code for implementation examples
4. Hardhat documentation for blockchain-specific questions

---

**Ready to start?** → Go to `stage4/gas-optimization/README.md` and begin Phase 1!

Good luck! 🚀

## 📚 Resources Yang Kamu Perlukan

**Untuk Phase 1 (Sekarang):**
- Akan dijelaskan saat kamu sampai di fase tersebut

## 🚦 Next Action

**MULAI SEKARANG:**
```bash
cd /home/sanul/projects/blockchain-engineer/stage4/polygon-deployment
cat QUICKSTART.md
```

Ikuti step-by-step guide di QUICKSTART.md untuk deploy ke Polygon Mumbai!

---

**Questions?** Tanya saja kalau ada yang kurang jelas. Good luck! 🚀
