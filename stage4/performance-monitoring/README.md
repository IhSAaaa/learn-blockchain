# Performance Monitoring

Monitor and benchmark the NFT marketplace performance on local Hardhat blockchain.

## Overview

Performance monitoring tools for:
- Contract execution times
- API response times
- Database query performance
- Transaction processing throughput
- Memory usage tracking

## What You'll Build

1. **Contract Performance Monitor**
   - Transaction execution time tracking
   - Gas usage per operation
   - Block mining time
   - State change impact analysis

2. **API Performance Metrics**
   - Response time per endpoint
   - Request/response size
   - Throughput measurements
   - Error rate tracking

3. **Benchmarking Suite**
   - Load testing
   - Stress testing
   - Capacity testing
   - Regression detection

4. **Monitoring Dashboard**
   - Real-time performance metrics
   - Historical trends
   - Performance alerts
   - Comparative analysis

## Tech Stack

**Backend Monitoring (Python)**
- Prometheus for metrics collection
- Flask-Prometheus for API metrics
- Custom decorators for function timing
- SQLite for metrics storage

**Visualization (React)**
- Grafana or custom React dashboard
- Real-time metric updates
- Performance trend graphs
- Alert notifications

## Getting Started

### 1. Setup Local Environment

```bash
cd stage4/performance-monitoring

# Backend setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Monitoring

```bash
# Start monitoring service
python monitor.py

# Collects metrics from:
# - Local Hardhat blockchain
# - Flask backend API
# - Database queries
# - Contract execution
```

### 3. View Metrics

```bash
# Access monitoring dashboard
# Frontend: http://localhost:3001
# Prometheus: http://localhost:9090
```

## Metrics to Track

### Smart Contract Metrics
- Deployment time
- Function call time
- State read/write time
- Gas usage trend
- Transaction confirmation time

### API Metrics
- Request latency
- Response size
- Throughput (requests/sec)
- Error rate
- Cache hit ratio

### System Metrics
- CPU usage
- Memory usage
- Disk I/O
- Network I/O
- Node uptime

## Performance Benchmarks

Create baseline performance benchmarks:

```bash
# Run benchmark suite
npm run benchmark

# Output: benchmark-results.json
# Contains baseline metrics for:
# - Deploy
# - Mint
# - List
# - Buy
# - Cancel
```

## Monitoring Setup

### Prometheus Configuration

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'flask-api'
    static_configs:
      - targets: ['localhost:5000']
  - job_name: 'hardhat'
    static_configs:
      - targets: ['localhost:8545']
```

### Custom Metrics

Track custom metrics for your application:

```python
# Flask endpoint metrics
from prometheus_client import Counter, Histogram

request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')

@app.route('/api/nfts/mint', methods=['POST'])
@request_duration.time()
def mint_nft():
    request_count.inc()
    # ... implementation
```

## Performance Testing

### Load Testing

```bash
# Simulate multiple users
npm run load-test

# Tests:
# - Mint 100 NFTs
# - List 50 NFTs
# - Buy 30 NFTs
# - Cancel 20 listings
```

### Stress Testing

```bash
# Push system to limits
npm run stress-test

# Gradually increase load until failure
# Identify bottlenecks and limits
```

## Analysis Tools

### Create Performance Report

```bash
# Generate performance analysis
python scripts/analyze-performance.py

# Output includes:
# - Performance trends
# - Bottleneck identification
# - Optimization recommendations
# - Comparison with baselines
```

## Optimization Recommendations

Based on monitoring data:
1. Identify slowest operations
2. Find bottlenecks (contract, API, DB)
3. Implement optimizations
4. Re-measure and verify improvements
5. Document changes

## Dashboard Views

1. **Overview**
   - Current performance summary
   - Key metrics at a glance

2. **Contracts**
   - Function execution times
   - Gas usage trends
   - Transaction throughput

3. **API**
   - Endpoint response times
   - Request volume
   - Error rates

4. **System**
   - Resource utilization
   - Network activity
   - Process health

## Workflow

```
┌─────────────────┐
│ Hardhat Node    │
│ (Port 8545)     │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Monitoring      │ → Collect metrics
│ Service         │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Prometheus      │ → Store metrics
│ (Port 9090)     │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Dashboard       │ → Visualize
│ (Port 3001)     │
└─────────────────┘
```

## Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Hardhat Gas Reporter](https://hardhat.org/plugins/nomiclabs-hardhat-gas-reporter)
- [Performance Optimization Tips](https://web.dev/performance/)

## Status

🚧 **Coming Soon** - Will be built after analytics dashboard is complete.

## Next Steps

1. Implement Prometheus metrics collection
2. Create monitoring dashboard
3. Build load testing suite
4. Generate performance reports
5. Document optimization findings
