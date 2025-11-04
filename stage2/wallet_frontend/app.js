// Global variables
let web3;
let ganacheWeb3; // Separate Web3 instance for Ganache
let contract;
let userAccount;
let contractAddress;
let contractAbi;

// --- CONFIGURATION ---
const DEPLOYMENT_FILE_PATH = '/deployment.json';
const GANACHE_URL = 'http://127.0.0.1:8545';

// --- INITIALIZATION ---

document.addEventListener('DOMContentLoaded', () => {
    log('Welcome to the Simple Greeter dApp!');
    if (typeof Web3 !== 'undefined') {
        log('✓ Web3.js library loaded');
    } else {
        log('⚠️ Web3.js not loaded yet', 'warning');
    }
});

async function connectWallet() {
    log('Attempting to connect wallet...');
    if (typeof window.ethereum !== 'undefined') {
        try {
            // Request account access
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            userAccount = accounts[0];
            web3 = new Web3(window.ethereum);
            
            // Create separate Web3 instance for Ganache (for reading contract state)
            ganacheWeb3 = new Web3(GANACHE_URL);
            log(`✓ Connected to Ganache at ${GANACHE_URL}`);

            // Update UI
            document.getElementById('connectionStatus').textContent = 'Connected';
            document.getElementById('connectionStatus').className = 'connected';
            document.getElementById('walletAddress').textContent = `${userAccount.substring(0, 6)}...${userAccount.substring(userAccount.length - 4)}`;
            log(`✅ Wallet connected: ${userAccount}`);

            // Initialize contract
            await initContract();

        } catch (error) {
            log(`❌ Wallet connection denied: ${error.message}`, 'error');
            document.getElementById('connectionStatus').textContent = 'Connection Failed';
        }
    } else {
        log('❌ MetaMask is not installed. Please install it to use this dApp.', 'error');
        document.getElementById('connectionStatus').textContent = 'MetaMask Not Found';
    }
}

async function initContract() {
    log('Initializing contract...');
    try {
        // Fetch the deployment file
        log(`Fetching deployment file from ${DEPLOYMENT_FILE_PATH}...`);
        const response = await fetch(DEPLOYMENT_FILE_PATH);
        if (!response.ok) {
            throw new Error(`Failed to fetch deployment file (${response.status})`);
        }
        const deploymentData = await response.json();
        
        contractAddress = deploymentData.address;
        contractAbi = deploymentData.abi;
        
        document.getElementById('contractAddress').textContent = contractAddress;
        log(`📄 Contract address: ${contractAddress}`);
        log(`📄 Contract ABI loaded with ${contractAbi.length} items`);

        // Create contract instance using Ganache for reads
        contract = new ganacheWeb3.eth.Contract(contractAbi, contractAddress);
        log('✅ Contract instance created (using Ganache provider).');

        // Read the initial greeting
        try {
            log('Reading initial greeting...');
            const greeting = await contract.methods.greeting().call();
            document.getElementById('currentGreeting').textContent = `"${greeting}"`;
            log(`✅ Initial greeting: ${greeting}`);
        } catch (readError) {
            log(`⚠️ Could not load initial greeting: ${readError.message}`, 'warning');
            document.getElementById('currentGreeting').textContent = 'Unable to load.';
        }

    } catch (error) {
        log(`❌ Contract initialization failed: ${error.message}`, 'error');
        document.getElementById('currentGreeting').textContent = 'Error loading contract.';
    }
}

// --- CONTRACT INTERACTION ---

async function getGreeting() {
    if (!contract || !ganacheWeb3) {
        log('Contract not initialized.', 'error');
        return;
    }
    log('Reading greeting from contract...');
    try {
        // Use Ganache provider for reading
        const result = await contract.methods.greeting().call();
        document.getElementById('currentGreeting').textContent = `"${result}"`;
        log(`✅ Greeting: ${result}`);
    } catch (error) {
        log(`Error reading contract: ${error.message}`, 'warning');
        document.getElementById('currentGreeting').textContent = 'Failed to load.';
    }
}

async function setGreeting() {
    if (!contract || !userAccount || !web3) {
        log('Wallet not connected or contract not initialized.', 'error');
        return;
    }
    const newGreeting = document.getElementById('newGreeting').value;
    if (!newGreeting) {
        log('Please enter a new greeting.', 'warning');
        return;
    }

    log(`Sending transaction to set greeting to: "${newGreeting}"`);
    try {
        // Use MetaMask provider for transactions
        const contractWithMetaMask = new web3.eth.Contract(contractAbi, contractAddress);
        const tx = await contractWithMetaMask.methods.setGreeting(newGreeting).send({ from: userAccount });
        log(`✅ Transaction confirmed! Hash: ${tx.transactionHash}`);
        document.getElementById('newGreeting').value = '';
        
        // Refresh greeting
        setTimeout(() => {
            getGreeting();
        }, 1000);

    } catch (error) {
        log(`❌ Transaction failed: ${error.message}`, 'error');
    }
}

// --- UTILITY FUNCTIONS ---

function log(message, type = 'info') {
    const logsContainer = document.getElementById('logs');
    const logEntry = document.createElement('p');
    const timestamp = new Date().toLocaleTimeString();
    
    logEntry.className = `log-entry log-${type}`;
    logEntry.textContent = `[${timestamp}] ${message}`;
    
    logsContainer.appendChild(logEntry);
    logsContainer.scrollTop = logsContainer.scrollHeight;
}

// Make functions globally accessible
window.connectWallet = connectWallet;
window.getGreeting = getGreeting;
window.setGreeting = setGreeting;
