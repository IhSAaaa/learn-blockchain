import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

// Components
import Header from './components/Header';
import Home from './pages/Home';
import Marketplace from './pages/Marketplace';
import MyNFTs from './pages/MyNFTs';
import CreateNFT from './pages/CreateNFT';

// Context
import { Web3Provider } from './context/Web3Context';

function App() {
  return (
    <Web3Provider>
      <Router>
        <div className="App">
          <Header />
          <main className="container-fluid">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/marketplace" element={<Marketplace />} />
              <Route path="/my-nfts" element={<MyNFTs />} />
              <Route path="/create" element={<CreateNFT />} />
            </Routes>
          </main>
        </div>
      </Router>
    </Web3Provider>
  );
}

export default App;