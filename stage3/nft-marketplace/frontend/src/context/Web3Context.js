import React, { createContext, useContext, useState, useEffect } from 'react';
import Web3 from 'web3';
import NFTMarketplaceABI from '../contracts/NFTMarketplace.json';

const Web3Context = createContext();

export const useWeb3 = () => {
  const context = useContext(Web3Context);
  if (!context) {
    throw new Error('useWeb3 must be used within a Web3Provider');
  }
  return context;
};

export const Web3Provider = ({ children }) => {
  const [web3, setWeb3] = useState(null);
  const [account, setAccount] = useState('');
  const [contract, setContract] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [networkId, setNetworkId] = useState(null);

  // Contract configuration
  const CONTRACT_ADDRESS = process.env.REACT_APP_CONTRACT_ADDRESS || '0x5FbDB2315678afecb367f032d93F642f64180aa3'; // Default to localhost
  const GANACHE_URL = 'http://127.0.0.1:8545';

  useEffect(() => {
    initWeb3();
  }, []);

  const initWeb3 = async () => {
    try {
      // Check if MetaMask is installed
      if (window.ethereum) {
        const web3Instance = new Web3(window.ethereum);
        setWeb3(web3Instance);

        // Get network ID
        const networkId = await web3Instance.eth.net.getId();
        setNetworkId(networkId);

        // Initialize contract with Ganache provider for reads
        const ganacheWeb3 = new Web3(GANACHE_URL);
        const contractInstance = new ganacheWeb3.eth.Contract(
          NFTMarketplaceABI,
          CONTRACT_ADDRESS
        );
        setContract(contractInstance);

      } else {
        setError('Please install MetaMask to use this dApp');
      }
    } catch (err) {
      setError('Failed to initialize Web3: ' + err.message);
    }
  };

  const connectWallet = async () => {
    try {
      setLoading(true);
      setError('');

      if (!web3) {
        throw new Error('Web3 not initialized');
      }

      // Request account access
      await window.ethereum.request({ method: 'eth_requestAccounts' });

      const accounts = await web3.eth.getAccounts();
      setAccount(accounts[0]);

      // Listen for account changes
      window.ethereum.on('accountsChanged', (accounts) => {
        setAccount(accounts[0] || '');
      });

      // Listen for network changes
      window.ethereum.on('chainChanged', (chainId) => {
        window.location.reload();
      });

    } catch (err) {
      setError('Failed to connect wallet: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const disconnectWallet = () => {
    setAccount('');
    setContract(null);
  };

  const switchToLocalNetwork = async () => {
    try {
      await window.ethereum.request({
        method: 'wallet_switchEthereumChain',
        params: [{ chainId: '0x539' }], // 1337 in hex
      });
    } catch (switchError) {
      // This error code indicates that the chain has not been added to MetaMask
      if (switchError.code === 4902) {
        try {
          await window.ethereum.request({
            method: 'wallet_addEthereumChain',
            params: [
              {
                chainId: '0x539',
                chainName: 'Localhost 8545',
                rpcUrls: ['http://127.0.0.1:8545'],
                nativeCurrency: {
                  name: 'ETH',
                  symbol: 'ETH',
                  decimals: 18,
                },
              },
            ],
          });
        } catch (addError) {
          setError('Failed to add network: ' + addError.message);
        }
      } else {
        setError('Failed to switch network: ' + switchError.message);
      }
    }
  };

  const getContractWithMetaMask = () => {
    if (!web3) return null;
    return new web3.eth.Contract(NFTMarketplaceABI, CONTRACT_ADDRESS);
  };

  const value = {
    web3,
    account,
    contract,
    loading,
    error,
    networkId,
    connectWallet,
    disconnectWallet,
    switchToLocalNetwork,
    getContractWithMetaMask,
    setError,
    setLoading,
  };

  return (
    <Web3Context.Provider value={value}>
      {children}
    </Web3Context.Provider>
  );
};