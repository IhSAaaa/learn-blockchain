#!/usr/bin/env python3
"""
Simple Blockchain Simulation
Stage 1: Basic blockchain simulation without consensus mechanism.
"""

import hashlib
import time
from datetime import datetime


class Block:
    """
    Represents a single block in the blockchain.
    
    Attributes:
        index (int): Position of the block in the chain.
        timestamp (str): Creation time of the block.
        data (str): Data stored in the block.
        previous_hash (str): Hash of the previous block.
        hash (str): Hash of the current block.
    """
    
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = datetime.now().isoformat()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate SHA-256 hash of the block."""
        block_str = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_str.encode()).hexdigest()
    
    def __str__(self):
        return f"""
Block #{self.index}
├─ Timestamp: {self.timestamp}
├─ Data: {self.data}
├─ Previous Hash: {self.previous_hash}
└─ Hash: {self.hash}
"""


class Blockchain:
    """Simple blockchain implementation."""
    
    def __init__(self):
        self.chain = []
        self._create_genesis_block()
    
    def _create_genesis_block(self):
        """Create the first block in the chain."""
        genesis = Block(0, "Genesis Block", "0")
        self.chain.append(genesis)
        print("✓ Genesis block created")
    
    def get_latest_block(self):
        """Return the most recent block."""
        return self.chain[-1]
    
    def add_block(self, data):
        """Add a new block to the chain."""
        latest = self.get_latest_block()
        new_block = Block(
            index=latest.index + 1,
            data=data,
            previous_hash=latest.hash
        )
        self.chain.append(new_block)
        return new_block
    
    def is_valid(self):
        """Validate the integrity of the blockchain."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            if current.hash != current.calculate_hash():
                print(f"✗ Block #{i}: Invalid hash")
                return False
            
            if current.previous_hash != previous.hash:
                print(f"✗ Block #{i}: Invalid previous hash reference")
                return False
        
        return True
    
    def print_chain(self):
        """Display all blocks in the chain."""
        print("\n" + "=" * 60)
        print("BLOCKCHAIN")
        print("=" * 60)
        for block in self.chain:
            print(block)
    
    def print_stats(self):
        """Display blockchain statistics."""
        print("\n" + "=" * 60)
        print("STATISTICS")
        print("=" * 60)
        print(f"Total Blocks: {len(self.chain)}")
        status = "✓ Valid" if self.is_valid() else "✗ Invalid"
        print(f"Chain Status: {status}")
        print("=" * 60)


def main():
    print("=" * 60)
    print("Simple Blockchain Simulator")
    print("=" * 60)
    print()
    
    blockchain = Blockchain()
    print()
    
    transactions = [
        "Alice sends 50 coins to Bob",
        "Bob sends 25 coins to Charlie",
        "Charlie sends 10 coins to Alice",
        "Alice sends 15 coins to David"
    ]
    
    print("Adding blocks to chain...\n")
    for tx in transactions:
        block = blockchain.add_block(tx)
        print(f"✓ Block #{block.index}: {tx}")
        time.sleep(0.5)
    
    blockchain.print_chain()
    blockchain.print_stats()
    
    print("\nInteractive mode:")
    print("Enter block data (type 'exit' to quit):\n")
    
    while True:
        user_data = input(">>> ")
        if user_data.lower() == 'exit':
            print("\nFinal chain state:")
            blockchain.print_chain()
            blockchain.print_stats()
            break
        
        block = blockchain.add_block(user_data)
        print(f"✓ Block #{block.index} added")
        print(f"  Hash: {block.hash}\n")


if __name__ == "__main__":
    main()
