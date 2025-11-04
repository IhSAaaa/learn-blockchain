import React from 'react';
import './MetricsCards.css';

function MetricsCards({ metrics }) {
  if (!metrics || metrics.error) {
    return (
      <div className="metrics-loading">
        <p>Waiting for metrics data...</p>
      </div>
    );
  }

  const cards = [
    {
      title: 'Total NFTs Minted',
      value: metrics.total_nfts_minted || 0,
      color: '#2196f3'
    },
    {
      title: 'Active Listings',
      value: metrics.active_listings || 0,
      color: '#673ab7'
    },
    {
      title: 'Total Sales',
      value: metrics.total_sales || 0,
      color: '#4caf50'
    },
    {
      title: 'Total Volume (ETH)',
      value: (metrics.total_volume_eth || 0).toFixed(2),
      color: '#ff9800'
    },
    {
      title: 'Unique Users',
      value: metrics.unique_users || 0,
      color: '#e91e63'
    },
    {
      title: 'Avg Price (ETH)',
      value: (metrics.average_price_eth || 0).toFixed(2),
      color: '#00bcd4'
    }
  ];

  return (
    <div className="metrics-grid">
      {cards.map((card, index) => (
        <div key={index} className="metric-card" style={{ borderLeftColor: card.color }}>
          <div className="metric-icon" style={{ backgroundColor: card.color + '20', borderColor: card.color }}>
            <div style={{ color: card.color }}>●</div>
          </div>
          <div className="metric-content">
            <p className="metric-title">{card.title}</p>
            <p className="metric-value">{card.value}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

export default MetricsCards;
