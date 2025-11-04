#!/usr/bin/env python3
"""
SHA-256 Hash Calculator
Stage 1: Demonstration of SHA-256 hashing algorithm with Python.
"""

import hashlib


def calculate_sha256(input_string):
    """
    Calculate SHA-256 hash from input string.
    
    Args:
        input_string (str): String to be hashed.
    
    Returns:
        str: SHA-256 hash in hexadecimal format.
    """
    return hashlib.sha256(input_string.encode()).hexdigest()


def main():
    """Main function to demonstrate SHA-256 hash calculator."""
    print("=" * 60)
    print("SHA-256 Hash Calculator - Stage 1 Blockchain Engineer")
    print("=" * 60)
    print()
    
    test_inputs = [
        "Hello, Blockchain!",
        "Bitcoin",
        "Ethereum",
        "Smart Contracts",
        ""
    ]
    
    print("SHA-256 Hash Demonstration:")
    print("-" * 60)
    
    for input_str in test_inputs:
        hash_result = calculate_sha256(input_str)
        display_input = input_str if input_str else "(empty string)"
        print(f"Input:  {display_input}")
        print(f"Hash:   {hash_result}")
        print(f"Length: {len(hash_result)} characters")
        print("-" * 60)
    
    print("\nInteractive Mode:")
    print("Enter a string to hash (type 'exit' to quit):")
    print()
    
    while True:
        user_input = input(">>> ")
        if user_input.lower() == 'exit':
            print("Thank you! Exiting program.")
            break
        
        hash_result = calculate_sha256(user_input)
        print(f"Hash: {hash_result}")
        print()


if __name__ == "__main__":
    main()
