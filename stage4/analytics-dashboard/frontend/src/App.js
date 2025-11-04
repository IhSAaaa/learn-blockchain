import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import './App.css';
import MetricsCards from './components/MetricsCards';
import TransactionsList from './components/TransactionsList';
import ChartsSection from './components/ChartsSection';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5001';

function App() {
  const [metrics, setMetrics] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [connected, setConnected] = useState(false);
  const [socket, setSocket] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initialize socket connection
    const newSocket = io(BACKEND_URL);
    
    newSocket.on('connect', () => {
      console.log('Connected to analytics backend');
      setConnected(true);
      setLoading(false);
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from analytics backend');
      setConnected(false);
    });

    newSocket.on('metrics_update', (data) => {
      console.log('Received metrics update:', data);
      setMetrics(data);
    });

    newSocket.on('transactions_update', (data) => {
      console.log('Received transactions update:', data);
      setTransactions(data.transactions || []);
    });

    setSocket(newSocket);

    // Cleanup on unmount
    return () => newSocket.close();
  }, []);

  useEffect(() => {
    if (!socket || !connected) return;

    // Request initial data
    socket.emit('request_metrics');
    socket.emit('request_transactions', { limit: 20 });

    // Set up periodic refresh
    const interval = setInterval(() => {
      socket.emit('request_metrics');
      socket.emit('request_transactions', { limit: 20 });
    }, 10000); // Refresh every 10 seconds

    return () => clearInterval(interval);
  }, [socket, connected]);

  const refreshData = () => {
    if (socket && connected) {
      socket.emit('request_metrics');
      socket.emit('request_transactions', { limit: 20 });
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Connecting to analytics service...</p>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>NFT Marketplace Analytics</h1>
        <div className="header-status">
          <span className={`status-indicator ${connected ? 'connected' : 'disconnected'}`}>
            {connected ? '● Live' : '● Offline'}
          </span>
          <button onClick={refreshData} className="refresh-btn" disabled={!connected}>
            Refresh
          </button>
        </div>
      </header>

      <main className="App-main">
        {!connected && (
          <div className="warning-banner">
            Not connected to analytics service. Make sure backend is running on {BACKEND_URL}
          </div>
        )}

        {metrics && metrics.error && (
          <div className="error-banner">
            {metrics.error}
          </div>
        )}

        <MetricsCards metrics={metrics} />
        <ChartsSection metrics={metrics} transactions={transactions} />
        <TransactionsList transactions={transactions} />
      </main>

      <footer className="App-footer">
        <p>NFT Marketplace Analytics Dashboard | Stage 4 - Phase 2</p>
        {metrics && metrics.timestamp && (
          <p className="last-update">Last updated: {new Date(metrics.timestamp).toLocaleString()}</p>
        )}
      </footer>
    </div>
  );
}

export default App;
