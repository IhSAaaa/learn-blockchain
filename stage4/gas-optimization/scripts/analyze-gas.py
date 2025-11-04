#!/usr/bin/env python3
"""
Gas Analysis Tool for NFT Marketplace
Analyzes gas report and identifies optimization opportunities
"""

import re
import sys
from pathlib import Path
from tabulate import tabulate

def parse_gas_report(file_path):
    """Parse gas report text file and extract metrics"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract method gas costs
    methods = {}
    
    # Pattern: |  NFTMarketplace  ·  methodName  ·  min  ·  max  ·  avg  ·  calls  ·  usd  |
    method_pattern = r'\|  NFTMarketplace\s+·\s+(\w+)\s+·\s+([\d-]+)\s+·\s+([\d-]+)\s+·\s+([\d-]+)\s+·\s+(\d+)\s+·'
    
    for match in re.finditer(method_pattern, content):
        method_name = match.group(1)
        min_gas = match.group(2)
        max_gas = match.group(3)
        avg_gas = match.group(4)
        calls = match.group(5)
        
        # Skip if no data
        if min_gas == '-':
            min_gas = avg_gas
            max_gas = avg_gas
        
        methods[method_name] = {
            'min': int(min_gas),
            'max': int(max_gas),
            'avg': int(avg_gas),
            'calls': int(calls)
        }
    
    # Extract deployment cost
    deployment_pattern = r'\|  NFTMarketplace\s+·\s+[\d-]+\s+·\s+[\d-]+\s+·\s+(\d+)\s+·'
    deployment_match = re.search(deployment_pattern, content)
    deployment_cost = int(deployment_match.group(1)) if deployment_match else 0
    
    return methods, deployment_cost

def analyze_and_recommend(methods, deployment_cost):
    """Analyze gas usage and provide optimization recommendations"""
    
    print("\n" + "="*80)
    print(" GAS ANALYSIS REPORT ".center(80, "="))
    print("="*80 + "\n")
    
    # 1. Deployment Analysis
    print("📦 DEPLOYMENT COST")
    print(f"   Gas Used: {deployment_cost:,}")
    print(f"   Percentage of Block Limit: {(deployment_cost / 30000000) * 100:.2f}%")
    if deployment_cost > 2000000:
        print("   ⚠️  High deployment cost - consider splitting contracts or optimization")
    print()
    
    # 2. Method Analysis
    print("⚡ METHOD GAS COSTS (sorted by average)")
    sorted_methods = sorted(methods.items(), key=lambda x: x[1]['avg'], reverse=True)
    
    table_data = []
    for method_name, data in sorted_methods:
        table_data.append([
            method_name,
            f"{data['min']:,}",
            f"{data['avg']:,}",
            f"{data['max']:,}",
            data['calls']
        ])
    
    print(tabulate(table_data, 
                   headers=['Method', 'Min Gas', 'Avg Gas', 'Max Gas', 'Calls'],
                   tablefmt='grid'))
    print()
    
    # 3. Top 3 Expensive Operations
    print("🔥 TOP 3 MOST EXPENSIVE OPERATIONS")
    for i, (method_name, data) in enumerate(sorted_methods[:3], 1):
        print(f"\n   {i}. {method_name}")
        print(f"      Average: {data['avg']:,} gas")
        print(f"      Called: {data['calls']} times")
        print(f"      Total Used: {data['avg'] * data['calls']:,} gas")
    print()
    
    # 4. Optimization Recommendations
    print("💡 OPTIMIZATION RECOMMENDATIONS")
    print()
    
    recommendations = []
    
    # Analyze each method
    for method_name, data in methods.items():
        if method_name == 'mintNFT' and data['avg'] > 100000:
            recommendations.append({
                'priority': 'HIGH',
                'method': method_name,
                'current': data['avg'],
                'issue': 'High minting cost',
                'solution': '1. Store tokenURI hash instead of full string\n'
                           '2. Use events for metadata (Index off-chain)\n'
                           '3. Batch mint multiple NFTs in one transaction'
            })
        
        if method_name == 'listNFT' and data['avg'] > 85000:
            recommendations.append({
                'priority': 'MEDIUM',
                'method': method_name,
                'current': data['avg'],
                'issue': 'Listing operation expensive',
                'solution': '1. Pack struct fields efficiently (use uint96 for price)\n'
                           '2. Avoid redundant storage writes\n'
                           '3. Use uint8 for boolean flags'
            })
        
        if method_name == 'buyNFT' and data['avg'] > 85000:
            recommendations.append({
                'priority': 'HIGH',
                'method': method_name,
                'current': data['avg'],
                'issue': 'Purchase flow has high gas',
                'solution': '1. Use unchecked arithmetic where overflow impossible\n'
                           '2. Cache storage reads in memory\n'
                           '3. Optimize fee calculation'
            })
    
    # General recommendations
    if deployment_cost > 1800000:
        recommendations.append({
            'priority': 'MEDIUM',
            'method': 'Deployment',
            'current': deployment_cost,
            'issue': 'Large contract size',
            'solution': '1. Enable Solidity optimizer (if not enabled)\n'
                       '2. Remove unused functions\n'
                       '3. Use libraries for shared code\n'
                       '4. Minimize string storage'
        })
    
    # Sort by priority
    priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
    recommendations.sort(key=lambda x: priority_order[x['priority']])
    
    for i, rec in enumerate(recommendations, 1):
        print(f"   [{rec['priority']}] {rec['method']}")
        print(f"   Current: {rec['current']:,} gas")
        print(f"   Issue: {rec['issue']}")
        print(f"   Solution:")
        for line in rec['solution'].split('\n'):
            print(f"      {line}")
        print()
    
    # 5. Estimated Savings
    print("📊 POTENTIAL SAVINGS")
    total_current = sum(m['avg'] * m['calls'] for m in methods.values())
    estimated_savings = int(total_current * 0.15)  # Conservative 15% estimate
    
    print(f"   Current Total Gas (all test operations): {total_current:,}")
    print(f"   Estimated Savings (10-20% optimization): {estimated_savings:,}")
    print(f"   Optimized Total: {total_current - estimated_savings:,}")
    print()
    
    # 6. Next Steps
    print("✅ NEXT STEPS")
    print("   1. Create optimized version of NFTMarketplace.sol")
    print("   2. Implement top 2-3 optimization techniques")
    print("   3. Run tests with REPORT_GAS=true again")
    print("   4. Compare results using compare-gas.py")
    print("   5. Document improvements in optimization-results.md")
    print()
    
    print("="*80)
    
    return recommendations

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze-gas.py <gas-report-file>")
        sys.exit(1)
    
    report_file = Path(sys.argv[1])
    if not report_file.exists():
        print(f"Error: File not found: {report_file}")
        sys.exit(1)
    
    methods, deployment_cost = parse_gas_report(report_file)
    recommendations = analyze_and_recommend(methods, deployment_cost)
    
    print(f"\n✨ Analysis complete! Found {len(recommendations)} optimization opportunities.\n")

if __name__ == '__main__':
    main()
