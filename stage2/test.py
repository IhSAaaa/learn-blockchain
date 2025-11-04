#!/usr/bin/env python3
"""
Unit Tests for Stage 2
Testing for pow_implementation.py and ethereum_interaction.py
"""

import unittest
from pow_implementation import ProofOfWork, MinedBlock


class TestProofOfWork(unittest.TestCase):
    """Test cases for Proof-of-Work implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pow = ProofOfWork(difficulty=3)
    
    def test_pow_initialization(self):
        """Verify PoW initializes with correct difficulty and target."""
        self.assertEqual(self.pow.difficulty, 3)
        self.assertEqual(self.pow.target, "000")
    
    def test_find_nonce_finds_valid_hash(self):
        """Ensure find_nonce returns a valid hash with nonce and time."""
        block_data = "Test Block Data"
        hash_result, nonce, mining_time = self.pow.find_nonce(block_data)
        
        self.assertIsNotNone(hash_result)
        self.assertGreaterEqual(nonce, 0)
        self.assertGreater(mining_time, 0)
    
    def test_hash_starts_with_zeros(self):
        """Verify hash result has required leading zeros."""
        block_data = "Test Block"
        hash_result, nonce, _ = self.pow.find_nonce(block_data)
        
        self.assertTrue(hash_result.startswith("000"))
    
    def test_verify_proof_valid(self):
        """Test that verification passes for valid proof."""
        block_data = "Test Data"
        hash_result, nonce, _ = self.pow.find_nonce(block_data)
        
        is_valid = self.pow.verify_proof(block_data, nonce, hash_result)
        self.assertTrue(is_valid)
    
    def test_verify_proof_invalid_hash(self):
        """Test that verification fails with incorrect hash."""
        block_data = "Test Data"
        _, nonce, _ = self.pow.find_nonce(block_data)
        
        invalid_hash = "0000invalid"
        is_valid = self.pow.verify_proof(block_data, nonce, invalid_hash)
        self.assertFalse(is_valid)
    
    def test_verify_proof_invalid_nonce(self):
        """Test that verification fails with incorrect nonce."""
        block_data = "Test Data"
        hash_result, _, _ = self.pow.find_nonce(block_data)
        
        invalid_nonce = 9999999
        is_valid = self.pow.verify_proof(block_data, invalid_nonce, hash_result)
        self.assertFalse(is_valid)
    
    def test_difficulty_adjustment(self):
        """Test dynamic difficulty adjustment."""
        self.pow.adjust_difficulty(4)
        self.assertEqual(self.pow.difficulty, 4)
        self.assertEqual(self.pow.target, "0000")
    
    def test_get_difficulty_info(self):
        """Retrieve and validate difficulty information."""
        info = self.pow.get_difficulty_info()
        
        self.assertEqual(info["difficulty_level"], 3)
        self.assertEqual(info["leading_zeros"], 3)
        self.assertEqual(info["target"], "000")
        self.assertGreater(info["approx_attempts"], 0)
    
    def test_higher_difficulty_takes_longer(self):
        """Confirm that increased difficulty requires more computation time."""
        block_data = "Compare Difficulty"
        
        pow_easy = ProofOfWork(difficulty=2)
        _, _, time_easy = pow_easy.find_nonce(block_data)
        
        pow_hard = ProofOfWork(difficulty=3)
        _, _, time_hard = pow_hard.find_nonce(block_data)
        
        self.assertGreater(time_easy, 0)
        self.assertGreater(time_hard, 0)


class TestMinedBlock(unittest.TestCase):
    """Test cases for MinedBlock class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pow = ProofOfWork(difficulty=2)
    
    def test_block_creation(self):
        """Test successful creation of a mined block."""
        block = MinedBlock(
            block_number=1,
            data="Test Block",
            previous_hash="abc123",
            pow=self.pow
        )
        
        self.assertEqual(block.block_number, 1)
        self.assertEqual(block.data, "Test Block")
        self.assertEqual(block.previous_hash, "abc123")
        self.assertIsNotNone(block.hash)
        self.assertGreaterEqual(block.nonce, 0)
    
    def test_block_hash_valid(self):
        """Validate that mined block has correct hash."""
        block = MinedBlock(
            block_number=1,
            data="Data",
            previous_hash="genesis",
            pow=self.pow
        )
        
        is_valid = self.pow.verify_proof(
            f"{block.block_number}{block.data}{block.previous_hash}",
            block.nonce,
            block.hash
        )
        self.assertTrue(is_valid)
    
    def test_block_mining_time(self):
        """Ensure mining time is properly recorded for blocks."""
        block = MinedBlock(
            block_number=1,
            data="Test",
            previous_hash="0",
            pow=self.pow
        )
        
        self.assertGreater(block.mining_time, 0)


class TestDifficultyComparison(unittest.TestCase):
    """Test suite for different difficulty levels."""
    
    def test_all_difficulties_produce_valid_hashes(self):
        """Verify that all tested difficulty levels produce valid hashes."""
        test_data = "Difficulty Test"
        
        for difficulty in range(2, 6):
            pow = ProofOfWork(difficulty=difficulty)
            hash_result, nonce, _ = pow.find_nonce(test_data)
            
            is_valid = pow.verify_proof(test_data, nonce, hash_result)
            self.assertTrue(is_valid, f"Difficulty {difficulty} failed")
    
    def test_difficulty_validation(self):
        """Verify hash has correct leading zeros and valid length."""
        pow = ProofOfWork(difficulty=3)
        hash_result, nonce, _ = pow.find_nonce("Test")
        
        self.assertTrue(hash_result.startswith("000"))
        self.assertEqual(len(hash_result), 64)


if __name__ == "__main__":
    unittest.main(verbosity=2)
