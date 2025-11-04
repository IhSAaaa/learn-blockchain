#!/usr/bin/env python3
"""
Performance Monitoring Service
Tracks system, API, and blockchain metrics
"""

import time
import psutil
import json
from datetime import datetime
from pathlib import Path

from prometheus_client import Counter, Histogram, Gauge, generate_latest
from web3 import Web3

# Prometheus metrics
request_count = Counter('api_requests_total', 'Total API requests')
request_duration = Histogram('api_request_duration_seconds', 'API request duration')
system_cpu = Gauge('system_cpu_percent', 'System CPU usage percentage')
system_memory = Gauge('system_memory_percent', 'System memory usage percentage')
blockchain_block = Gauge('blockchain_current_block', 'Current blockchain block number')

# Web3 connection
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'system': {},
            'blockchain': {},
            'api': {},
            'timestamp': None
        }
        
    def collect_system_metrics(self):
        """Collect system performance metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        system_cpu.set(cpu_percent)
        system_memory.set(memory.percent)
        
        self.metrics['system'] = {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_used_mb': memory.used / (1024 * 1024),
            'memory_total_mb': memory.total / (1024 * 1024),
            'disk_percent': disk.percent,
            'disk_used_gb': disk.used / (1024 * 1024 * 1024),
            'disk_total_gb': disk.total / (1024 * 1024 * 1024)
        }
        
        return self.metrics['system']
    
    def collect_blockchain_metrics(self):
        """Collect blockchain metrics"""
        if not w3.is_connected():
            return {'error': 'Not connected to blockchain'}
        
        try:
            block_number = w3.eth.block_number
            block = w3.eth.get_block('latest')
            
            blockchain_block.set(block_number)
            
            self.metrics['blockchain'] = {
                'current_block': block_number,
                'gas_limit': block.gasLimit,
                'gas_used': block.gasUsed,
                'gas_usage_percent': (block.gasUsed / block.gasLimit * 100),
                'timestamp': block.timestamp
            }
            
            return self.metrics['blockchain']
        except Exception as e:
            return {'error': str(e)}
    
    def collect_all_metrics(self):
        """Collect all metrics"""
        self.collect_system_metrics()
        self.collect_blockchain_metrics()
        self.metrics['timestamp'] = datetime.now().isoformat()
        
        return self.metrics
    
    def get_prometheus_metrics(self):
        """Generate Prometheus metrics"""
        return generate_latest()

def main():
    monitor = PerformanceMonitor()
    
    print("="*60)
    print(" Performance Monitoring Service ".center(60, "="))
    print("="*60)
    print("\n📊 Monitoring started...")
    print(f"   Hardhat URL: http://127.0.0.1:8545")
    print(f"   Metrics endpoint: http://localhost:9090/metrics")
    print("\n" + "="*60 + "\n")
    
    try:
        while True:
            metrics = monitor.collect_all_metrics()
            
            # Print metrics
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Metrics Update")
            print(f"  CPU: {metrics['system']['cpu_percent']:.1f}%")
            print(f"  Memory: {metrics['system']['memory_percent']:.1f}%")
            
            if 'error' not in metrics['blockchain']:
                print(f"  Block: {metrics['blockchain']['current_block']}")
                print(f"  Gas Usage: {metrics['blockchain']['gas_usage_percent']:.1f}%")
            else:
                print(f"  Blockchain: {metrics['blockchain']['error']}")
            
            time.sleep(5)  # Update every 5 seconds
            
    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped\n")

if __name__ == '__main__':
    main()
