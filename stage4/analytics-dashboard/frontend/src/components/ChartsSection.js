import React from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import './ChartsSection.css';

function ChartsSection({ metrics, transactions }) {
  if (!metrics || !transactions) {
    return null;
  }

  // Prepare data for transaction type distribution
  const txTypeData = transactions.reduce((acc, tx) => {
    const existing = acc.find(item => item.name === tx.type);
    if (existing) {
      existing.value++;
    } else {
      acc.push({ name: tx.type.toUpperCase(), value: 1 });
    }
    return acc;
  }, []);

  // Colors for pie chart
  const COLORS = {
    MINT: '#2196f3',
    LIST: '#673ab7',
    SALE: '#4caf50'
  };

  // Prepare data for sales over time (by block ranges)
  const salesByBlock = transactions
    .filter(tx => tx.type === 'sale')
    .reduce((acc, tx) => {
      const blockRange = Math.floor(tx.block / 100) * 100;
      const existing = acc.find(item => item.block === blockRange);
      if (existing) {
        existing.sales++;
        existing.volume += tx.price_eth;
      } else {
        acc.push({
          block: blockRange,
          sales: 1,
          volume: tx.price_eth
        });
      }
      return acc;
    }, [])
    .sort((a, b) => a.block - b.block);

  // Price distribution
  const priceRanges = [
    { range: '0-0.5 ETH', min: 0, max: 0.5, count: 0 },
    { range: '0.5-1 ETH', min: 0.5, max: 1, count: 0 },
    { range: '1-2 ETH', min: 1, max: 2, count: 0 },
    { range: '2+ ETH', min: 2, max: Infinity, count: 0 }
  ];

  transactions
    .filter(tx => tx.type === 'sale' || tx.type === 'list')
    .forEach(tx => {
      const price = tx.price_eth;
      const range = priceRanges.find(r => price >= r.min && price < r.max);
      if (range) range.count++;
    });

  return (
    <div className="charts-section">
      <div className="chart-container">
        <h3>Transaction Type Distribution</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={txTypeData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {txTypeData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[entry.name] || '#6b7280'} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {salesByBlock.length > 0 && (
        <div className="chart-container">
          <h3>Sales Activity Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={salesByBlock}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="block" label={{ value: 'Block Range', position: 'insideBottom', offset: -5 }} />
              <YAxis label={{ value: 'Number of Sales', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="sales" stroke="#4caf50" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      <div className="chart-container">
        <h3>Price Range Distribution</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={priceRanges}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="range" />
            <YAxis label={{ value: 'Count', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#2196f3" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {salesByBlock.length > 0 && (
        <div className="chart-container">
          <h3>Trading Volume Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={salesByBlock}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="block" label={{ value: 'Block Range', position: 'insideBottom', offset: -5 }} />
              <YAxis label={{ value: 'Volume (ETH)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="volume" fill="#ff9800" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

export default ChartsSection;
