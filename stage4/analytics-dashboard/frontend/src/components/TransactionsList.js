import React from 'react';
import './TransactionsList.css';

function TransactionsList({ transactions }) {
  if (!transactions || transactions.length === 0) {
    return (
      <div className="transactions-container">
        <h2>Recent Transactions</h2>
        <div className="transactions-empty">
          <p>No transactions yet. Start minting, listing, or buying NFTs!</p>
        </div>
      </div>
    );
  }

  const getTransactionLabel = (type) => {
    switch (type) {
      case 'mint':
        return 'Mint';
      case 'list':
        return 'List';
      case 'sale':
        return 'Sale';
      default:
        return 'Transaction';
    }
  };

  const getTransactionColor = (type) => {
    switch (type) {
      case 'mint':
        return '#2196f3';
      case 'list':
        return '#673ab7';
      case 'sale':
        return '#4caf50';
      default:
        return '#757575';
    }
  };

  const formatAddress = (address) => {
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  };

  return (
    <div className="transactions-container">
      <h2>Recent Transactions</h2>
      <div className="transactions-list">
        {transactions.map((tx, index) => (
          <div key={index} className="transaction-item">
            <div 
              className="transaction-icon" 
              style={{ 
                backgroundColor: getTransactionColor(tx.type) + '20',
                borderColor: getTransactionColor(tx.type)
              }}
            >
              <span style={{ color: getTransactionColor(tx.type) }}>
                {getTransactionLabel(tx.type)}
              </span>
            </div>
            
            <div className="transaction-details">
              <div className="transaction-header">
                <span className="transaction-type" style={{ color: getTransactionColor(tx.type) }}>
                  {tx.type.toUpperCase()}
                </span>
                <span className="transaction-token">Token #{tx.token_id}</span>
              </div>
              
              <div className="transaction-info">
                {tx.type === 'mint' && (
                  <p>Minted by {formatAddress(tx.address)}</p>
                )}
                {tx.type === 'list' && (
                  <p>Listed by {formatAddress(tx.seller)} for {tx.price_eth} ETH</p>
                )}
                {tx.type === 'sale' && (
                  <p>
                    Sold to {formatAddress(tx.buyer)} for {tx.price_eth} ETH
                  </p>
                )}
              </div>
              
              <div className="transaction-meta">
                <span>Block #{tx.block}</span>
                <span className="transaction-hash" title={tx.tx_hash}>
                  {formatAddress(tx.tx_hash)}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TransactionsList;
