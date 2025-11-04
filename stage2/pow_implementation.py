#!/usr/bin/env python3
"""
Proof-of-Work (PoW) Implementation
Stage 2: Mining algorithm simulation and understanding difficulty mechanics
"""

import hashlib
import time
from typing import Tuple


class ProofOfWork:
    """
    Proof-of-Work mining algorithm implementation.
    Demonstrates how Bitcoin and blockchain mining operates.
    """
    
    def __init__(self, difficulty: int = 4):
        """
        Initialize PoW with a specified difficulty level.
        
        Args:
            difficulty (int): Number of leading zeros required in hash.
                            Default: 4 (hash must start with 0000)
        """
        self.difficulty = difficulty
        self.target = "0" * difficulty
    
    def find_nonce(self, block_data: str) -> Tuple[str, int, float]:
        """
        Mine a block by finding a nonce that produces a hash with required leading zeros.
        
        Args:
            block_data (str): The block data to be mined.
        
        Returns:
            Tuple[str, int, float]: (resulting hash, nonce value, mining time in seconds)
        """
        nonce = 0
        start_time = time.time()
        
        print(f"\n{'='*60}")
        print(f"Mining Block (Difficulty: {self.difficulty})")
        print(f"Target: {self.target}...")
        print(f"{'='*60}\n")
        
        while True:
            candidate = f"{block_data}{nonce}"
            hash_value = hashlib.sha256(candidate.encode()).hexdigest()
            
            if hash_value.startswith(self.target):
                elapsed = time.time() - start_time
                return hash_value, nonce, elapsed
            
            nonce += 1
            
            if nonce % 100000 == 0:
                elapsed = time.time() - start_time
                print(f"Attempts: {nonce:,} | Elapsed: {elapsed:.2f}s | Hash: {hash_value}")
    
    def verify_proof(self, block_data: str, nonce: int, block_hash: str) -> bool:
        """
        Verify that a proof-of-work is valid.
        
        Args:
            block_data (str): The block data.
            nonce (int): The nonce found during mining.
            block_hash (str): The hash to verify.
        
        Returns:
            bool: True if proof is valid, False otherwise.
        """
        candidate = f"{block_data}{nonce}"
        calculated_hash = hashlib.sha256(candidate.encode()).hexdigest()
        
        return (calculated_hash == block_hash and 
                calculated_hash.startswith(self.target))
    
    def adjust_difficulty(self, new_difficulty: int):
        """
        Adjust the difficulty level (simulates network difficulty adjustment).
        
        Args:
            new_difficulty (int): The new difficulty level.
        """
        self.difficulty = new_difficulty
        self.target = "0" * new_difficulty
        print(f"Difficulty adjusted to: {new_difficulty}")
    
    def get_difficulty_info(self) -> dict:
        """Retrieve information about current difficulty settings."""
        return {
            "difficulty_level": self.difficulty,
            "leading_zeros": self.difficulty,
            "target": self.target,
            "approx_attempts": 16 ** self.difficulty
        }


class MinedBlock:
    """Represents a block that has been mined using Proof-of-Work."""
    
    def __init__(self, block_number: int, data: str, previous_hash: str, pow: ProofOfWork):
        """
        Create and mine a new block.
        
        Args:
            block_number (int): The block number.
            data (str): Transaction data contained in the block.
            previous_hash (str): Hash of the previous block.
            pow (ProofOfWork): ProofOfWork instance for mining.
        """
        self.block_number = block_number
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        
        block_content = f"{block_number}{data}{previous_hash}"
        self.hash, self.nonce, self.mining_time = pow.find_nonce(block_content)
    
    def __str__(self):
        """String representation of the mined block."""
        return f"""
Block #{self.block_number}
├─ Data: {self.data}
├─ Previous Hash: {self.previous_hash}
├─ Nonce: {self.nonce}
├─ Hash: {self.hash}
└─ Mining Time: {self.mining_time:.3f}s
"""


def compare_difficulties():
    """Demonstrate the impact of different difficulty levels on mining."""
    print("\n" + "="*60)
    print("DIFFICULTY LEVEL COMPARISON")
    print("="*60 + "\n")
    
    test_data = "Sample Transaction Block"
    
    for difficulty in range(2, 6):
        print(f"\n{'─'*60}")
        print(f"Difficulty: {difficulty}")
        print(f"{'─'*60}")
        
        pow = ProofOfWork(difficulty=difficulty)
        info = pow.get_difficulty_info()
        
        print(f"Target: {info['target']}...")
        print(f"Expected attempts: {info['approx_attempts']:,}")
        
        start = time.time()
        hash_result, nonce, mining_time = pow.find_nonce(test_data)
        
        print(f"\n✓ Block mined!")
        print(f"  Hash: {hash_result}")
        print(f"  Nonce: {nonce:,}")
        print(f"  Time: {mining_time:.3f}s")


def main():
    """Main entry point for PoW demonstration."""
    print("="*60)
    print("Proof-of-Work Implementation - Stage 2")
    print("="*60)
    
    print("\n" + "="*60)
    print("DEMO 1: Mining a Single Block")
    print("="*60)
    
    pow = ProofOfWork(difficulty=4)
    block = MinedBlock(
        block_number=1,
        data="Alice sends 50 coins to Bob",
        previous_hash="0000abc123",
        pow=pow
    )
    print(block)
    
    is_valid = pow.verify_proof(
        f"1Alice sends 50 coins to Bob0000abc123",
        block.nonce,
        block.hash
    )
    print(f"✓ Verification: {'Valid' if is_valid else 'Invalid'}")
    
    compare_difficulties()
    
    print("\n" + "="*60)
    print("DEMO 2: Interactive Mining")
    print("="*60 + "\n")
    
    difficulty_input = input("Enter difficulty level (2-5, default 3): ").strip()
    difficulty = int(difficulty_input) if difficulty_input.isdigit() else 3
    difficulty = max(2, min(5, difficulty))
    
    pow_custom = ProofOfWork(difficulty=difficulty)
    custom_data = input("Enter block data: ").strip() or "My Custom Block"
    
    print(f"\nMining with difficulty {difficulty}...")
    block_custom = MinedBlock(
        block_number=1,
        data=custom_data,
        previous_hash="genesis",
        pow=pow_custom
    )
    print(block_custom)
    
    is_valid = pow_custom.verify_proof(
        f"1{custom_data}genesis",
        block_custom.nonce,
        block_custom.hash
    )
    print(f"✓ Verification: {'Valid' if is_valid else 'Invalid'}")


if __name__ == "__main__":
    main()
