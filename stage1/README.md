# Stage 1: Personal Notes — Blockchain Engineer Fundamentals

## A Brief Story

I'm working on Stage 1 as a practical introduction to understanding blockchain basics using Python. Here I'm trying two simple but important things: creating a SHA-256 hash calculator and building a lightweight blockchain simulator. This writing is like a small journal — what I built, why, and how to test it.

## Project Structure (brief notes)
This is the folder structure I created for experimentation:

```
stage1/
├── hash_calculator.py          # SHA-256 Calculator
├── blockchain_simulator.py     # Simple blockchain simulation
├── test_stage1.py              # Unit tests for both components
├── README.md                   # Notes you're reading now
└── requirements.txt            # Dependencies (if needed)
```

## File Contents — Story Per File

### 1. hash_calculator.py
This is a small utility I created to compute SHA-256 hashes from string input. Initially just to see hash properties — determinism, fixed size, and how changing one character can change the entire hash.

Features I built:
- calculate_sha256() to compute the hash
- demo mode with several examples I mentioned
- interactive mode if you want to type input yourself

Running:
```bash
python hash_calculator.py
```

Example output (I used examples for readability):
```
============================================================
SHA-256 Hash Calculator - Stage 1 Blockchain Engineer
============================================================

SHA-256 Hash Demo:
------------------------------------------------------------
Input:  Hello, Blockchain!
Hash:   7f83b1657ff1fc53b92dc18148a1d65dfa13514a9fbe8b9d8f6a1b9c4f5d6e7a
Length: 64 characters
------------------------------------------------------------
```

### 2. blockchain_simulator.py
This is the most fun part for me: assembling blocks, connecting them via hashes, then checking chain integrity. No consensus mechanism here — focus on basic structure and validation.

Features:
- Block class: represents a block with automatic hash computation
- Blockchain class: manages the chain of blocks
- Genesis block automatically created on initialization
- Validation function to detect changes/tampering
- Interactive mode to add new blocks

Running:
```bash
python blockchain_simulator.py
```

Example output (like notes when I tested):
```
============================================================
Simple Blockchain Simulation - Stage 1
============================================================

✓ Genesis Block created!

Adding blocks to blockchain...

✓ Block #1 added: Alice sends 50 coins to Bob
✓ Block #2 added: Bob sends 25 coins to Charlie

============================================================
BLOCKCHAIN CHAIN
============================================================

Block #0
├─ Timestamp: 2025-11-03T10:30:45.123456
├─ Data: Genesis Block
├─ Previous Hash: 0
└─ Hash: a3f5c6d8e9b7a1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c

...

============================================================
BLOCKCHAIN STATISTICS
============================================================
Total Blocks: 4
Chain Valid: ✓ Valid
============================================================
```

### 3. test_stage1.py
I wrote unit tests so small changes don't break the foundation I've built. Running tests makes me more confident that basic functions remain correct.

Test coverage:
- TestHashCalculator: several tests to ensure determinism and different inputs produce different hashes
- TestBlock: testing block creation and hash computation
- TestBlockchain: testing block addition, chain validation, and tampering detection

Running:
```bash
python -m pytest test_stage1.py -v
```
or
```bash
python test_stage1.py
```

Things being tested:
- SHA-256 always produces the same value for identical input
- Block structure and hash consistency
- Inter-block linking (previous_hash) integrity
- Changes to block content are detected by validator

## Core Concepts — My Brief Notes

1. Hashing (SHA-256)
    - Cryptographic function that transforms input into a fixed-length string.
    - Important properties: deterministic, hard to reverse, highly sensitive to small changes (avalanche effect).
    - In blockchain: used to create unique block identifiers and maintain chain integrity.

2. Block Structure
    Each block I created contains:
    ```
    Block = {
         index: integer,           # position in chain
         timestamp: string,        # creation time
         data: string,             # payload (e.g., transactions)
         previous_hash: string,    # hash of previous block
         hash: string              # SHA-256 of this block
    }
    ```

3. Blockchain Architecture
    Blocks are linked together via previous_hash. If one block changes, its hash changes and the link to the next block no longer matches — this is the basis for tampering detection.

4. Chain Integrity
    - Validation checks two main things: whether each block's hash is correct (based on content) and whether each block's previous_hash matches the previous block's hash.
    - If either fails, the chain is considered broken.

## Brief Requirements
- Python 3.7+
- Core functionality requires no external dependencies
- pytest useful for testing (optional)

## Getting Started (brief)
```bash
cd stage1
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt   # if needed
```

## Usage — Practical Notes
Run demos:
```bash
python hash_calculator.py
python blockchain_simulator.py
```

Run tests:
```bash
python test_stage1.py
# or
pytest test_stage1.py -v
```

Example usage in other code:
```python
from hash_calculator import calculate_sha256
from blockchain_simulator import Blockchain

h = calculate_sha256("Hello, World!")
chain = Blockchain()
chain.add_block("Transaction 1")
if chain.is_valid():
     print("Chain valid — congratulations!")
```

## Learning Objectives (what I covered)
- Understanding how SHA-256 works
- Basic blockchain structure
- How blocks are linked together
- Chain integrity validation and tampering detection

## Next Steps (personal notes)
After feeling comfortable with these basics, I want to move to Stage 2: learning Proof-of-Work, interacting with Ethereum via Web3.py, and trying to deploy contracts on testnet.

## Sources I Read
- https://en.wikipedia.org/wiki/SHA-2
- https://docs.python.org/3/library/hashlib.html
- https://bitcoin.org/en/how-it-works
- Mastering Bitcoin (community reference)

## Author
Ihsanul Maulana  
raflyade27@gmail.com

Note: this is part of "Blockchain Engineer Learning Path - Stage 1"

## License
MIT License — Free to use and modify for learning purposes

