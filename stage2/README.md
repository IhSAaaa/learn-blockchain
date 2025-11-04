# Stage 2: Diving into Blockchain (Blockchain Foundations)

## About Stage 2

So at this stage I'm diving straight into the real blockchain world. Not theory anymore, but hands-on with Proof-of-Work, Web3, and smart contracts. This is the moment where everything starts clicking—when abstract concepts become tangible things I can experiment with.

There are four main things I want to master here:

1. **Proof-of-Work Implementation** - Mining simulator, so I understand how blockchain validates blocks
2. **Ethereum Interaction** - Using Web3.py to query blockchain directly
3. **Smart Contracts** - Writing and deploying contracts in Solidity
4. **Wallet Frontend** - Building a UI to interact with blockchain

## Project Structure

Here's how the folder is organized:

```
stage2/
├── pow_implementation.py              # My mining simulator
├── ethereum_interaction.py            # Web3 client for blockchain queries
├── test_stage2.py                     # Unit tests, crucial for validation
├── smart_contract/
│   ├── SimpleGreeter.sol             # Simple Solidity contract
│   ├── deploy.py                     # Script to deploy to blockchain
│   └── interact.py                   # Script to interact with contract
├── wallet_frontend/
│   ├── index.html                    # Wallet UI
│   ├── app.js                        # Web3.js logic
│   └── style.css                     # Styling
├── README.md                          # This notes file
├── requirements.txt                   # Python dependencies
└── .gitignore                         # Git ignore
```

## Files I'm Working On

### 1. pow_implementation.py

This file contains the mining algorithm implementation. I built this to really understand how miners work—searching for the right nonce until getting a hash with leading zeros.

**What's inside:**
- `ProofOfWork` class - Mining engine with adjustable difficulty
- `MinedBlock` class - Represents a successfully mined block

**Features:**
- Finding valid nonce
- Verifying proof-of-work
- Adjusting difficulty when needed
- Comparing difficulty levels

**How to run:**
```bash
python3 pow_implementation.py
```

Output looks roughly like this:
```
============================================================
Proof-of-Work (PoW) Implementation - Stage 2
============================================================

============================================================
DEMO 1: Mining Single Block
============================================================

============================================================
Mining Block (Difficulty: 4)
Target: 0000...
============================================================

Attempts: 100,000 | Time: 2.34s | Hash: 000abc...
Attempts: 200,000 | Time: 4.56s | Hash: 000def...

Block #1
├─ Data: Alice sends 50 coins to Bob
├─ Previous Hash: 0000abc123
├─ Nonce: 347,923
├─ Hash: 0000def456789...
└─ Mining Time: 6.789s

✓ Block verification: Valid
```

### 2. ethereum_interaction.py

This is the file I use to talk directly to the blockchain. Using Web3.py library, which is powerful enough to interact with Ethereum nodes.

**Main class:**
- `EthereumClient` - All blockchain operations are here

**Available methods:**
- `get_connection_status()` - Check if connected to node
- `create_account()` - Generate new wallet
- `get_balance()` - Check balance of an address
- `get_account_info()` - Full account details
- `send_transaction()` - Send ETH to another address
- `get_transaction_details()` - Check transaction details
- `estimate_gas()` - Estimate how much gas is needed

**Before running, need to setup:**
```bash
# Install Web3.py first
pip install web3 eth-account

# Two options:
# 1. Local node with Ganache
npm install -g ganache
ganache

# 2. Or use testnet (Sepolia)
# Use Infura, Alchemy, or QuickNode API key
```

**How to run:**
```bash
python3 ethereum_interaction.py
```

### 3. smart_contract/SimpleGreeter.sol

A Solidity contract I built as a learning project. Simple but covers important concepts like state variables, events, and access control.

**What it can do:**
- Set greeting message
- Get the latest greeting
- Track history of all greetings
- Only owner can set greeting (access control)
- Event logging for each change

**Easiest way to deploy:**
1. Go to https://remix.ethereum.org
2. Copy-paste code from SimpleGreeter.sol
3. Compile (Ctrl+S)
4. Deploy to testnet using MetaMask

### 4. smart_contract/deploy.py

Script to deploy contract to blockchain. This is automation for me, so I don't need to do it manually in Remix.

**What it does:**
- Compile contract
- Deploy with constructor arguments
- Save deployment info (address, ABI, etc.)

**How to run:**
```bash
python3 smart_contract/deploy.py
```

### 5. smart_contract/interact.py

Script to interact with deployed contracts. Can call both read and write functions.

**Features:**
- Call read functions (view, pure)
- Call write functions (state-changing)
- Listen to events
- Interactive mode for experimenting

**How to run:**
```bash
python3 smart_contract/interact.py
```

### 6. wallet_frontend/

Web-based wallet I built using Web3.js. Simple but functional for learning purposes.

**What it can do:**
- Connect to network
- Generate new wallet
- Check balance
- Send transaction
- View transaction details
- Activity log

**Setup:**
```bash
# Open in browser or use HTTP server
python3 -m http.server 8000
# Then open http://localhost:8000/wallet_frontend
```

### 7. test_stage2.py

Test suite to make sure all components work as expected. I built this for sanity checking.

**Test cases:**
- PoW initialization runs
- Nonce finding logic is correct
- Hash verification is accurate
- Difficulty adjustment works
- Block mining from start to finish
- Network connection is stable

**How to run:**
```bash
python3 test_stage2.py
```

## 📚 Concepts I'm Learning

### 1. Proof-of-Work (PoW)

This is the "heart" of blockchain security. The concept is simple but powerful: miners must find a nonce (number once) that makes the hash have leading zeros.

**How it works:**
- Miners take block data
- Add nonce
- Hash everything
- Check if hash has required leading zeros
- If yes, block is valid. If no, increment nonce and repeat

**Difficulty relationship:**
```
Difficulty 2: Hash starts with "00"
Average attempts: ~256

Difficulty 3: Hash starts with "000"
Average attempts: ~4,096

Difficulty 4: Hash starts with "0000"
Average attempts: ~65,536
```

So the higher the difficulty, the longer mining takes. This maintains a consistent block time.

### 2. Web3.py - Ethereum Interaction

Web3.py is a powerful library for talking to the Ethereum blockchain. I use it for:

**Connection management:**
- Connect to local node or remote RPC
- Check if connected

**Account operations:**
- Create new wallet
- Import existing wallet
- Manage multiple accounts

**Blockchain queries:**
```python
web3.eth.get_block_number()       # Latest block
web3.eth.get_balance(address)     # Balance at address
web3.eth.get_transaction(tx_hash) # Transaction details
web3.eth.send_raw_transaction()   # Send transaction
```

**Gas and transactions:**
- Estimate gas for transaction
- Send transaction to blockchain
- Monitor transaction status

### 3. Smart Contracts - Solidity

This is the language for writing logic that runs on the blockchain. Important to understand some concepts:

**State Variables:** Storage that persists on blockchain. When state changes, blockchain records everything.

**Functions:**
- Public: Can be called from anywhere
- Private: Only from contract itself
- View: Read-only, don't change state
- Pure: Don't read or change state

**Events:** Logging mechanism. Important events are emitted, so they can be listened to from frontend.

**Modifiers:** Pattern to add conditions. For example `onlyOwner` to restrict access to owner only.

**ABI (Application Binary Interface):** Interface between contract and the outside world. This is what I use to interact from Python or JavaScript.

**SimpleGreeter contract I built:**
```solidity
function setGreeting(string newGreeting) public
function getGreeting() public returns (string)
function getMyGreetings() public view returns (string[])
event GreetingUpdated(address updater, string newGreeting, uint256 timestamp)
```

### 4. Web3.js - Frontend Integration

Web3.js is the sibling of Web3.py but for JavaScript/browser. I use it for:

**Provider connection:**
- Connect to MetaMask
- Connect to custom RPC node

**Contract interaction:**
- Call contract functions
- Listen to events
- Send transactions

**Account management:**
- Import wallet
- Sign transactions
- Manage multiple accounts

**Transaction handling:**
- Build transaction
- Estimate gas
- Sign and send
- Monitor status

## Setup & Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher (for npm tools)
- MetaMask browser extension (optional, for wallet_frontend)
- Solidity compiler (solc) - required for contract compilation
- Git (for version control)

### Step-by-Step Setup

#### 1. Clone and Navigate to Stage 2
```bash
git clone <your-repo>
cd blockchain-engineer/stage2
```

#### 2. Create Python Virtual Environment
```bash
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate          # Linux/Mac
# OR
venv\Scripts\activate             # Windows
```

#### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `web3.py` - Core library for Ethereum interaction
- `eth-account` - Account management and signing
- `py-solc-x` - Solidity compiler wrapper (optional)
- `pytest` - Testing framework

#### 4. Setup Solidity Compiler (solc)
```bash
# For Linux/Mac with brew
brew install solidity

# For Windows
# Download from: https://github.com/ethereum-optimism/solc-bin
# Or use solcx Python package:
python3 -c "import solcx; solcx.install_solc('0.8.0')"
```

#### 5. Setup Local Ethereum Node (Optional but Recommended)
```bash
# Install Ganache globally
npm install -g ganache

# Start Ganache in separate terminal
ganache
# Output: Listening on 127.0.0.1:8545
```

**Ganache provides:**
- 10 pre-funded test accounts (100 ETH each)
- Chain ID: 1337
- Gas price: 2 Gwei
- All transactions are instant

#### 6. Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your settings:
# - PROVIDER_URL: Your Ethereum RPC endpoint
# - DEPLOYER_ADDRESS: Your account address
# - PRIVATE_KEY: Your private key (NEVER commit this!)
```

#### 7. Verify Installation
```bash
# Run tests
python3 -m pytest test.py -v

# Expected: 14 passed in ~3 seconds
```

---

## Complete Workflow Guide

This section shows the complete flow from smart contract development to interaction.

### Workflow Overview
```
SimpleGreeter.sol
        ↓
    compile
        ↓
  deploy.py (creates artifacts)
        ↓
  bin/SimpleGreeter.json (contains ABI & address)
        ↓
interact.py OR app.js (reads from artifacts)
        ↓
   Results / State Changes
```

### Option 1: Python-Based Workflow

#### Step A: Deploy Contract with Python
```bash
cd smart_contract
python3 deploy.py
```

**Interactive prompts:**
1. Select "1. Deploy SimpleGreeter"
2. Enter initial greeting (default: "Hello")
3. Enter your deployer address (from Ganache or testnet)
4. Enter your private key (WITHOUT 0x prefix)
5. Wait for confirmation

**Output:**
```
Connected to provider: http://127.0.0.1:8545

============================================================
Deploy SimpleGreeter
============================================================

Transaction sent. Hash: 0x...
Waiting for confirmation...

Success!
Address: 0x...
Tx: 0x...
Block: 42

Saved to deployment.json
```

**Created files:**
- `deployment.json` - Contains contract address, ABI, and metadata
- `bin/stage2/smart_contract/SimpleGreeter.abi` - Extracted ABI
- `bin/stage2/smart_contract/SimpleGreeter.json` - Full contract artifact

#### Step B: Interact with Contract (Python)
```bash
python3 interact.py
```

**Interactive options:**
```
Options:
  1 - Read current greeting
  2 - Update greeting (requires signature)
  3 - Exit
```

**Example interaction:**
```
Select: 1
Greeting: "Hello"

Select: 2
New greeting: "Hello Blockchain!"
Your address: 0x...
Private key: your_private_key

Transaction sent
Hash: 0x...
```

### Option 2: Web-Based Workflow (Frontend)

#### Step A: Ensure Contract is Deployed
First, deploy using `deploy.py` to create deployment artifacts.

#### Step B: Open Frontend
```bash
# Option 1: Direct open
cd wallet_frontend
open index.html  # macOS
# OR
start index.html # Windows
# OR
xdg-open index.html # Linux

# Option 2: HTTP Server (Recommended)
cd ..
python3 -m http.server 8000
# Then navigate to http://localhost:8000/wallet_frontend
```

#### Step C: Connect Wallet
1. Install MetaMask extension (if not already installed)
2. On the page, click "Connect MetaMask"
3. Approve connection in MetaMask popup
4. Select network (must match deployment network)

#### Step D: Interact with Contract
- **Get Balance**: Shows current account balance
- **Generate Wallet**: Creates new test account
- **Read Greeting**: Calls view function
- **Update Greeting**: Sends transaction (requires gas)

---

## 🔍 Understanding the Deploy -> Interact Workflow

### What Happens During Deployment

1. **Compilation Phase**
   ```python
   compiled = deployer.compile_contract("SimpleGreeter.sol")
   # Returns: {"abi": [...], "bytecode": "0x..."}
   ```

2. **Transaction Building**
   ```python
   tx = constructor.build_transaction({
       "from": deployer_address,
       "nonce": 42,
       "gas": 1000000,
       "gasPrice": 2000000000  # 2 Gwei
   })
   ```

3. **Transaction Signing**
   ```python
   signed_tx = w3.eth.account.sign_transaction(tx, private_key)
   ```

4. **Transaction Sending & Receipt**
   ```python
   tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
   receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
   # Returns: {"contractAddress": "0x...", "status": 1, ...}
   ```

5. **Artifact Saving**
   - Contract address from receipt
   - ABI from compilation
   - Both saved to `deployment.json`

### What Happens During Interaction

1. **Load Artifacts**
   ```python
   with open("deployment.json") as f:
       deployment = json.load(f)
   contract_address = deployment["address"]
   abi = deployment["abi"]
   ```

2. **Create Contract Instance**
   ```python
   contract = w3.eth.contract(address=contract_address, abi=abi)
   ```

3. **Read-Only Calls (View Functions)**
   ```python
   result = contract.functions.getGreeting().call()
   # No transaction, instant return
   ```

4. **State-Changing Calls (Write Functions)**
   ```python
   tx = contract.functions.setGreeting("New").build_transaction({...})
   signed_tx = w3.eth.account.sign_transaction(tx, private_key)
   tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
   ```

---

## 📋 Configuration Reference

### Environment Variables (.env)

```ini
# Ethereum Node Configuration
PROVIDER_URL=http://127.0.0.1:8545          # Local: Ganache
# PROVIDER_URL=https://sepolia.infura.io/v3/YOUR_KEY  # Testnet: Sepolia

# Account Configuration
DEPLOYER_ADDRESS=0x...                      # Your account address
PRIVATE_KEY=your_private_key_without_0x    # WARNING: NEVER commit!

# Optional: Alternative RPC Providers
# ALCHEMY_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY
# QUICKNODE_URL=https://your-endpoint.quiknode.pro
```

### Ganache Configuration

Ganache automatically provides 10 test accounts:
```
Account 0: 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1
           Private Key: 0x4f3edf983ac636a65a842ce7c78d9aa706d3b113d26dada3cff76ec46d3d3679

Account 1: 0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0
           Private Key: 0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6b5a93e869f99b57e02afe1

...and 8 more accounts
```

All accounts have 100 ETH balance for testing.

### RPC Provider Comparison

| Provider | Testnet | Speed | Free Tier | Setup |
|----------|---------|-------|-----------|-------|
| Ganache | Local | Instant | ∞ | `ganache` |
| Infura | Sepolia | ~12s | Limited | API Key needed |
| Alchemy | Sepolia | ~12s | 300M units | API Key needed |
| Hardhat | Local | Instant | ∞ | `npx hardhat node` |

## Practical Learning

### Scenario 1: Mining a Block

This is the most fun part. I run the script and watch how the nonce increments until getting a valid hash.

```bash
python3 pow_implementation.py
# Choose difficulty level (2-5)
# Watch progress
# See final nonce and hash
```

**Observation:** Difficulty 4 takes much longer than difficulty 2. Exponential growth. Awesome!

### Scenario 2: Query Ethereum

```bash
python3 ethereum_interaction.py
# 1. Check connection to node
# 2. Generate new wallet
# 3. Check balance
# 4. Query transaction details
```

### Scenario 3: Deploy Contract

```bash
python3 smart_contract/deploy.py
# 1. Compile contract
# 2. Set initial greeting message
# 3. Deploy to testnet
# 4. Save deployment info
```

### Scenario 4: Use Wallet Frontend

1. Open `wallet_frontend/index.html` in browser
2. Connect MetaMask (or use Infura provider)
3. Generate new wallet or import existing
4. Check balance
5. Send test transaction to another address (testnet only!)

## 🔗 Testnet Setup

### Sepolia Testnet

This is the latest testnet I recommend. Sepolia is the active one now.

- **Chain ID**: 11155111
- **RPC**: https://sepolia.infura.io/v3/YOUR_KEY
- **Faucet**: https://sepoliafaucet.com
- **Explorer**: https://sepolia.etherscan.io

### Goerli Testnet

This is already deprecated, so I'll skip it.

- **Chain ID**: 5

### Local Blockchain (Ganache)

For local development, Ganache is very convenient.

- **Chain ID**: 1337 (or 31337 for Hardhat)
- **RPC**: http://127.0.0.1:8545
- **Pre-funded accounts**: Automatically has 10 accounts with ETH balance

## Security Notes I Remember

1. **NEVER SHARE private keys** - This isn't a joke. Whoever has the private key has full control.
2. **Testnet only** - Never experiment on mainnet until 100% confident
3. **Keep keys in .env** - Never hardcode private keys in code
4. **Double-check address** - Blockchain transactions are irreversible. Check 3x before sending
5. **Estimate gas first** - Don't be surprised by a huge gas bill

---

## Testing & Validation

### Unit Tests

Run all unit tests:
```bash
python3 -m pytest test.py -v
```

Expected output (14 tests):
```
stage2/test.py::TestProofOfWork::test_pow_initialization PASSED          [  7%]
stage2/test.py::TestProofOfWork::test_find_nonce_finds_valid_hash PASSED [ 14%]
...
stage2/test.py::TestDifficultyComparison::test_difficulty_validation PASSED [100%]

============================== 14 passed in 3.20s ==============================
```

### Integration Tests

Test deploy and interact workflow together:
```bash
cd smart_contract
python3 -m pytest integration_test.py -v
```

**Integration tests cover:**
- ✅ Contract compilation
- ✅ Deployment with mocked blockchain
- ✅ Read-only function calls
- ✅ State-changing transactions
- ✅ Event retrieval
- ✅ Artifact persistence
- ✅ Complete workflow sequence

### Testing on Actual Blockchain

To test on Ganache or testnet:

```bash
# 1. Start Ganache (if using local)
ganache

# 2. In another terminal, run deployment test
python3 -c "
from deploy import ContractDeployer
deployer = ContractDeployer('http://127.0.0.1:8545')
# Get first Ganache account
accounts = deployer.w3.eth.accounts
print(f'Using account: {accounts[0]}')
print(f'Balance: {deployer.w3.eth.get_balance(accounts[0])} wei')
"
```

---

## Common Tasks & Examples

### Task 1: Deploy to Local Ganache

```python
from deploy import ContractDeployer

deployer = ContractDeployer("http://127.0.0.1:8545")

# Get test account from Ganache
test_account = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
test_private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113d26dada3cff76ec46d3d3679"

result = deployer.deploy_contract(
    "SimpleGreeter",
    ["Hello Ganache"],
    test_account,
    test_private_key
)

if result["success"]:
    print(f"Deployed to: {result['contract_address']}")
else:
    print(f"Error: {result['error']}")
```

### Task 2: Call Read Function

```python
from interact import ContractInteractor
import json

interactor = ContractInteractor("http://127.0.0.1:8545")

# Load deployment artifact
with open("deployment.json") as f:
    deployment = json.load(f)

result = interactor.call_function(
    deployment["address"],
    deployment["abi"],
    "getGreeting"
)

if result["success"]:
    print(f"Current greeting: {result['result']}")
```

### Task 3: Send Transaction

```python
from interact import ContractInteractor
import json

interactor = ContractInteractor("http://127.0.0.1:8545")

with open("deployment.json") as f:
    deployment = json.load(f)

# Use same Ganache account
test_account = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
test_private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113d26dada3cff76ec46d3d3679"

result = interactor.send_transaction(
    deployment["address"],
    deployment["abi"],
    "setGreeting",
    test_account,
    test_private_key,
    ["New Greeting"]
)

if result["success"]:
    print(f"Transaction: {result['tx_hash']}")
    print(f"Block: {result['block_number']}")
    print(f"Gas used: {result['gas_used']}")
```

### Task 4: Deploy to Sepolia Testnet

```bash
# 1. Get Sepolia ETH from faucet
# https://sepoliafaucet.com

# 2. Create account and save in .env
# PROVIDER_URL=https://sepolia.infura.io/v3/YOUR_INFURA_KEY
# DEPLOYER_ADDRESS=your_account_address
# PRIVATE_KEY=your_private_key_without_0x

# 3. Deploy
python3 deploy.py
```

---

## 🐛 Troubleshooting Guide

### Issue: "Cannot connect to provider"

**Symptoms:**
```
Warning: Cannot connect to http://127.0.0.1:8545
```

**Solutions:**
1. **If using Ganache:**
   ```bash
   # Check if Ganache is running
   ps aux | grep ganache
   
   # If not, start it
   ganache
   ```

2. **If using Infura:**
   ```bash
   # Check your API key
   echo $PROVIDER_URL  # Should show full URL with key
   
   # Verify format:
   # https://sepolia.infura.io/v3/YOUR_KEY_HERE
   ```

3. **If using custom RPC:**
   ```bash
   # Test connection
   curl -X POST http://your-rpc:8545 -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
   ```

### Issue: "Web3 Module Not Found"

```
ModuleNotFoundError: No module named 'web3'
```

**Solution:**
```bash
# Install missing packages
pip install -r requirements.txt

# Or install individually
pip install web3 eth-account eth-keys eth-typing eth-utils
```

### Issue: "Private Key Invalid"

```
ValueError: Invalid private key
```

**Causes and Solutions:**
```python
# ❌ WRONG: Include 0x prefix
private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113d26dada3cff76ec46d3d3679"

# ✅ CORRECT: Without 0x prefix
private_key = "4f3edf983ac636a65a842ce7c78d9aa706d3b113d26dada3cff76ec46d3d3679"

# Or use with Web3
from web3 import Web3
private_key_bytes = bytes.fromhex(private_key)  # Without 0x
```

### Issue: "Insufficient Gas"

```
Exception: Gas estimation failed - {'code': -32000, 'message': 'exceeds block gas limit'}
```

**Solution:**
```python
# Increase gas limit in transaction
tx = {
    "from": account,
    "nonce": nonce,
    "gas": 3000000,  # Increased from 1000000
    "gasPrice": web3.eth.gas_price
}
```

### Issue: "Nonce Too Low"

```
Exception: {'code': -32000, 'message': 'nonce too low'}
```

**Causes and Solutions:**
- Transaction already processed
- Nonce is out of sync

```python
# Get fresh nonce each time
nonce = w3.eth.get_transaction_count(address)

# If stuck, reset Ganache
ganache --deterministic --accounts 10
```

### Issue: "Cannot Find Deployment.json"

```
FileNotFoundError: [Errno 2] No such file or directory: 'deployment.json'
```

**Solution:**
```bash
# Make sure you're in smart_contract directory
cd stage2/smart_contract

# Run deploy first
python3 deploy.py

# Then interact
python3 interact.py
```

### Issue: "Contract Address Invalid"

```
ValueError: Invalid address format
```

**Solution:**
```python
# Contract address must be valid Ethereum address
from web3 import Web3

address = "0x1234..."
if Web3.is_address(address):
    checksum_address = Web3.to_checksum_address(address)
else:
    print("Invalid address!")
```

### Issue: "MetaMask Not Connecting to Frontend"

**Solutions:**
1. Check MetaMask is installed and unlocked
2. Ensure network is selected (check dropdown)
3. Open browser console (F12) for error messages
4. Try refreshing page
5. Check if running on localhost:8000 or similar

```javascript
// Debug in browser console
console.log(typeof window.ethereum);  // Should be 'object'
console.log(window.ethereum.chainId); // Should show chain ID
```

---

## 📚 Security Best Practices

### Private Key Management

```bash
# ❌ NEVER DO THIS
# Don't hardcode in source code
PRIVATE_KEY = "0x..."

# ✅ DO THIS INSTEAD
# Use .env file (add to .gitignore)
PRIVATE_KEY=... (in .env file only)

# Or use environment variable
export PRIVATE_KEY=...
```

### Testnet vs Mainnet

```python
# ✅ Always verify network
chain_id = w3.eth.chain_id

if chain_id == 1:
    raise Exception("NEVER use mainnet for testing!")
elif chain_id in [5, 11155111]:  # Goerli, Sepolia
    print("✓ Using testnet - safe")
elif chain_id == 1337:
    print("✓ Using Ganache - safe")
```

### Transaction Verification

```python
# ✅ Always verify before sending
print(f"Sending {amount} from {from_addr} to {to_addr}")
print(f"Gas price: {gas_price} Gwei")
print(f"Estimated cost: {gas_price * gas_limit} Gwei")
response = input("Confirm? (yes/no): ")

if response.lower() != "yes":
    print("Transaction cancelled")
    return
```

---

## 🎓 What I Master After Stage 2

✅ How Proof-of-Work mining actually works  
✅ Relationship between difficulty and mining time  
✅ Web3.py for querying blockchain  
✅ Account and wallet management basics  
✅ Smart contracts fundamentals  
✅ ABI and how to interact with contracts  
✅ Signing transactions and sending to blockchain  
✅ Gas estimation and optimization  
✅ Deploying to testnet and local blockchain  
- Web3.js for frontend integration  
- Deploy → Interact workflow  
- Integration testing for blockchain code  

## Next Steps

After Stage 2, I'm ready to move to **Stage 3: Build DApps**

Plans:
- Build NFT marketplace (full-stack)
- Build DeFi lending protocol
- Deploy to production
- Polish UI/UX
- Security audit basics

## Helpful Resources

- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Solidity by Example](https://solidity-by-example.org/)
- [Ethereum.org Developers](https://ethereum.org/en/developers/)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)
- [Remix IDE](https://remix.ethereum.org/)
- [Sepolia Testnet Faucet](https://sepoliafaucet.com/)
- [Ganache Documentation](https://www.trufflesuite.com/ganache)
- [Ethers.js (alternative to Web3.js)](https://docs.ethers.io/)

## Important Notes

- I run tests with difficulty 2-3 for speed
- PoW implementation is educational, not production-ready
- Web3.py requires node connection for some operations
- Smart contract deployment requires testnet ETH (free from faucet)
- Always use testnet or local blockchain during development
- Never commit private keys or sensitive credentials

---
