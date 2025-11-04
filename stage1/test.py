#!/usr/bin/env python3
"""
Unit Tests for Stage 1 Projects
Testing for hash_calculator.py and blockchain_simulator.py
"""

import unittest
import hashlib
from hash_calculator import calculate_sha256
from blockchain_simulator import Block, Blockchain


class TestHashCalculator(unittest.TestCase):
    """Test cases for hash calculator."""
    
    def test_sha256_basic(self):
        """Test SHA-256 hash calculation with basic input."""
        result = calculate_sha256("Hello")
        expected = hashlib.sha256("Hello".encode()).hexdigest()
        self.assertEqual(result, expected)
    
    def test_sha256_empty_string(self):
        """Test SHA-256 hash calculation with empty string."""
        result = calculate_sha256("")
        expected = hashlib.sha256("".encode()).hexdigest()
        self.assertEqual(result, expected)
    
    def test_sha256_long_string(self):
        """Test SHA-256 hash calculation with long string."""
        long_string = "a" * 1000
        result = calculate_sha256(long_string)
        expected = hashlib.sha256(long_string.encode()).hexdigest()
        self.assertEqual(result, expected)
    
    def test_sha256_output_length(self):
        """Test that SHA-256 output is always 64 characters."""
        result = calculate_sha256("test")
        self.assertEqual(len(result), 64)
    
    def test_sha256_deterministic(self):
        """Test that SHA-256 is deterministic (same output for same input)."""
        input_str = "Blockchain"
        result1 = calculate_sha256(input_str)
        result2 = calculate_sha256(input_str)
        self.assertEqual(result1, result2)
    
    def test_sha256_different_inputs(self):
        """Test that different inputs produce different hashes."""
        hash1 = calculate_sha256("Bitcoin")
        hash2 = calculate_sha256("Ethereum")
        self.assertNotEqual(hash1, hash2)


class TestBlock(unittest.TestCase):
    """Test cases for Block class."""
    
    def test_block_creation(self):
        """Test creating a new block."""
        block = Block(0, "Test Data", "0")
        self.assertEqual(block.index, 0)
        self.assertEqual(block.data, "Test Data")
        self.assertEqual(block.previous_hash, "0")
        self.assertIsNotNone(block.hash)
    
    def test_block_hash_calculation(self):
        """Test that block hash is calculated correctly."""
        block = Block(1, "Test", "previous_hash")
        recalculated_hash = block.calculate_hash()
        self.assertEqual(block.hash, recalculated_hash)
    
    def test_block_hash_length(self):
        """Test that block hash is 64 characters (SHA-256)."""
        block = Block(0, "Data", "0")
        self.assertEqual(len(block.hash), 64)
    
    def test_different_blocks_different_hashes(self):
        """Test that different blocks have different hashes."""
        block1 = Block(0, "Data1", "0")
        block2 = Block(0, "Data2", "0")
        self.assertNotEqual(block1.hash, block2.hash)


class TestBlockchain(unittest.TestCase):
    """Test cases for Blockchain class."""
    
    def setUp(self):
        """Set up blockchain for each test."""
        self.blockchain = Blockchain()
    
    def test_genesis_block_creation(self):
        """Test genesis block creation."""
        self.assertEqual(len(self.blockchain.chain), 1)
        genesis = self.blockchain.chain[0]
        self.assertEqual(genesis.index, 0)
        self.assertEqual(genesis.data, "Genesis Block")
        self.assertEqual(genesis.previous_hash, "0")
    
    def test_add_single_block(self):
        """Test adding a single block to blockchain."""
        self.blockchain.add_block("Test Data")
        self.assertEqual(len(self.blockchain.chain), 2)
    
    def test_add_multiple_blocks(self):
        """Test adding multiple blocks to blockchain."""
        for i in range(5):
            self.blockchain.add_block(f"Block {i}")
        self.assertEqual(len(self.blockchain.chain), 6)
    
    def test_block_chain_linkage(self):
        """Test that blocks are correctly linked together."""
        self.blockchain.add_block("Block 1")
        self.blockchain.add_block("Block 2")
        
        block1 = self.blockchain.chain[1]
        block2 = self.blockchain.chain[2]
        
        self.assertEqual(block2.previous_hash, block1.hash)
    
    def test_get_latest_block(self):
        """Test getting the latest block."""
        self.blockchain.add_block("Block 1")
        self.blockchain.add_block("Block 2")
        
        latest = self.blockchain.get_latest_block()
        self.assertEqual(latest.index, 2)
        self.assertEqual(latest.data, "Block 2")
    
    def test_blockchain_valid(self):
        """Test validation of a valid blockchain."""
        self.blockchain.add_block("Block 1")
        self.blockchain.add_block("Block 2")
        self.blockchain.add_block("Block 3")
        
        self.assertTrue(self.blockchain.is_valid())
    
    def test_blockchain_invalid_hash(self):
        """Test validation of blockchain with modified hash."""
        self.blockchain.add_block("Block 1")
        self.blockchain.chain[1].hash = "invalid_hash"
        
        self.assertFalse(self.blockchain.is_valid())
    
    def test_blockchain_invalid_previous_hash(self):
        """Test validation of blockchain with modified previous_hash."""
        self.blockchain.add_block("Block 1")
        self.blockchain.add_block("Block 2")
        
        self.blockchain.chain[1].previous_hash = "invalid_hash"
        
        self.assertFalse(self.blockchain.is_valid())


if __name__ == "__main__":
    unittest.main(verbosity=2)
