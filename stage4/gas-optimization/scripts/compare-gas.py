#!/usr/bin/env python3
"""
Gas Comparison Tool
Compares baseline vs optimized gas reports
"""

import re
import sys
from pathlib import Path
from tabulate import tabulate

def parse_gas_report(file_path):
    """Parse gas report and extract metrics"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    methods = {}
    method_pattern = r'\|  NFTMarketplace\s+·\s+(\w+)\s+·\s+([\d-]+)\s+·\s+([\d-]+)\s+·\s+([\d-]+)\s+·\s+(\d+)\s+·'
    
    for match in re.finditer(method_pattern, content):
        method_name = match.group(1)
        avg_gas = match.group(4)
        
        if avg_gas != '-':
            methods[method_name] = int(avg_gas)
    
    deployment_pattern = r'\|  NFTMarketplace\s+·\s+[\d-]+\s+·\s+[\d-]+\s+·\s+(\d+)\s+·'
    deployment_match = re.search(deployment_pattern, content)
    deployment_cost = int(deployment_match.group(1)) if deployment_match else 0
    
    return methods, deployment_cost

def compare_reports(baseline_file, optimized_file):
    """Compare two gas reports and show improvements"""
    
    baseline_methods, baseline_deploy = parse_gas_report(baseline_file)
    optimized_methods, optimized_deploy = parse_gas_report(optimized_file)
    
    print("\n" + "="*90)
    print(" GAS OPTIMIZATION RESULTS ".center(90, "="))
    print("="*90 + "\n")
    
    # Deployment comparison
    print("📦 DEPLOYMENT COST")
    deploy_diff = baseline_deploy - optimized_deploy
    deploy_pct = (deploy_diff / baseline_deploy * 100) if baseline_deploy > 0 else 0
    
    print(f"   Baseline:  {baseline_deploy:,} gas")
    print(f"   Optimized: {optimized_deploy:,} gas")
    print(f"   Savings:   {deploy_diff:,} gas ({deploy_pct:+.2f}%)")
    
    if deploy_pct > 0:
        print("   ✅ Deployment optimized!")
    elif deploy_pct < 0:
        print("   ⚠️  Deployment cost increased")
    print()
    
    # Method comparison
    print("⚡ METHOD GAS COMPARISON")
    
    table_data = []
    total_baseline = 0
    total_optimized = 0
    
    all_methods = set(baseline_methods.keys()) | set(optimized_methods.keys())
    
    for method in sorted(all_methods):
        baseline_gas = baseline_methods.get(method, 0)
        optimized_gas = optimized_methods.get(method, 0)
        
        if baseline_gas > 0:
            diff = baseline_gas - optimized_gas
            pct = (diff / baseline_gas * 100) if baseline_gas > 0 else 0
            
            status = "✅" if pct > 0 else "⚠️" if pct < 0 else "➖"
            
            table_data.append([
                method,
                f"{baseline_gas:,}",
                f"{optimized_gas:,}",
                f"{diff:+,}",
                f"{pct:+.2f}%",
                status
            ])
            
            total_baseline += baseline_gas
            total_optimized += optimized_gas
    
    print(tabulate(table_data,
                   headers=['Method', 'Baseline', 'Optimized', 'Savings', 'Change %', 'Status'],
                   tablefmt='grid'))
    print()
    
    # Overall summary
    print("📊 OVERALL SUMMARY")
    total_diff = total_baseline - total_optimized
    total_pct = (total_diff / total_baseline * 100) if total_baseline > 0 else 0
    
    print(f"   Total Baseline Gas:  {total_baseline:,}")
    print(f"   Total Optimized Gas: {total_optimized:,}")
    print(f"   Total Savings:       {total_diff:,} gas")
    print(f"   Average Reduction:   {total_pct:.2f}%")
    print()
    
    # Achievement badges
    print("🏆 ACHIEVEMENTS")
    achievements = []
    
    if total_pct >= 20:
        achievements.append("⭐⭐⭐ Excellent! 20%+ gas reduction")
    elif total_pct >= 15:
        achievements.append("⭐⭐ Great! 15%+ gas reduction")
    elif total_pct >= 10:
        achievements.append("⭐ Good! 10%+ gas reduction")
    elif total_pct >= 5:
        achievements.append("👍 Nice! 5%+ gas reduction")
    else:
        achievements.append("💡 Some savings achieved")
    
    if deploy_pct > 10:
        achievements.append("📦 Deployment significantly optimized")
    
    # Check specific methods
    for method, baseline in baseline_methods.items():
        if method in optimized_methods:
            optimized = optimized_methods[method]
            method_pct = ((baseline - optimized) / baseline * 100)
            
            if method == 'mintNFT' and method_pct > 15:
                achievements.append("🎨 Minting highly optimized")
            if method == 'buyNFT' and method_pct > 10:
                achievements.append("💰 Purchase flow optimized")
    
    for achievement in achievements:
        print(f"   {achievement}")
    print()
    
    print("="*90 + "\n")

def main():
    if len(sys.argv) < 3:
        print("Usage: python compare-gas.py <baseline-report> <optimized-report>")
        sys.exit(1)
    
    baseline_file = Path(sys.argv[1])
    optimized_file = Path(sys.argv[2])
    
    if not baseline_file.exists():
        print(f"Error: Baseline file not found: {baseline_file}")
        sys.exit(1)
    
    if not optimized_file.exists():
        print(f"Error: Optimized file not found: {optimized_file}")
        sys.exit(1)
    
    compare_reports(baseline_file, optimized_file)
    print("✨ Comparison complete!\n")

if __name__ == '__main__':
    main()
