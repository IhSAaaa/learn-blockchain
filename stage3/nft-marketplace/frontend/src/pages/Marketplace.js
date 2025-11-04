import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Badge, Alert, Spinner } from 'react-bootstrap';
import { useWeb3 } from '../context/Web3Context';

const Marketplace = () => {
  const { contract, account, getContractWithMetaMask, setError, setLoading } = useWeb3();
  const [nfts, setNfts] = useState([]);
  const [loading, setLoadingState] = useState(false);

  useEffect(() => {
    if (contract) {
      loadMarketplaceNFTs();
    }
  }, [contract]);

  const loadMarketplaceNFTs = async () => {
    try {
      setLoadingState(true);
      setError('');

      // In a real implementation, you'd need to track all listed NFTs
      // For now, we'll simulate with some example NFTs
      const mockNFTs = [
        {
          tokenId: 0,
          tokenURI: 'https://via.placeholder.com/300x250/FF6B6B/FFFFFF?text=NFT+1',
          name: 'Cosmic Dream #1',
          description: 'A beautiful cosmic dream artwork',
          price: '1.5',
          seller: '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
          isActive: true
        },
        {
          tokenId: 1,
          tokenURI: 'https://via.placeholder.com/300x250/4ECDC4/FFFFFF?text=NFT+2',
          name: 'Digital Landscape #2',
          description: 'Stunning digital landscape',
          price: '2.0',
          seller: '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
          isActive: true
        }
      ];

      // In production, you'd query events or maintain an off-chain index
      setNfts(mockNFTs);
    } catch (err) {
      setError('Failed to load marketplace NFTs: ' + err.message);
    } finally {
      setLoadingState(false);
    }
  };

  const buyNFT = async (tokenId, price) => {
    try {
      setLoading(true);
      setError('');

      if (!account) {
        throw new Error('Please connect your wallet first');
      }

      const contractWithMetaMask = getContractWithMetaMask();
      if (!contractWithMetaMask) {
        throw new Error('Contract not available');
      }

      const priceInWei = contract.methods.web3.utils.toWei(price, 'ether');

      await contractWithMetaMask.methods.buyNFT(tokenId).send({
        from: account,
        value: priceInWei,
        gas: 300000
      });

      // Reload marketplace after purchase
      await loadMarketplaceNFTs();

      alert('NFT purchased successfully!');
    } catch (err) {
      setError('Failed to buy NFT: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price) => {
    return `${price} ETH`;
  };

  const formatAddress = (address) => {
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  };

  return (
    <Container className="py-4">
      <Row className="mb-4">
        <Col>
          <h2 style={{color: '#1f2937', fontWeight: '600'}}>Marketplace</h2>
          <p style={{color: '#6b7280'}}>Discover and purchase NFTs</p>
        </Col>
      </Row>

      {loading && (
        <Row className="justify-content-center mb-4">
          <Col xs="auto">
            <Spinner animation="border" variant="primary" size="sm" />
            <span className="ms-2" style={{color: '#6b7280'}}>Loading...</span>
          </Col>
        </Row>
      )}

      <Row className="g-4">
        {nfts.map((nft) => (
          <Col key={nft.tokenId} md={6} lg={4}>
            <Card className="nft-card">
              <Card.Img
                variant="top"
                src={nft.tokenURI}
                className="nft-image"
                alt={nft.name}
              />
              <Card.Body>
                <div className="d-flex justify-content-between align-items-start mb-2">
                  <Card.Title className="mb-0" style={{color: '#1f2937', fontSize: '1.1rem', fontWeight: '600'}}>
                    {nft.name}
                  </Card.Title>
                  <Badge bg="primary" style={{fontSize: '0.85rem'}}>{formatPrice(nft.price)}</Badge>
                </div>
                <Card.Text className="mb-3" style={{color: '#6b7280', fontSize: '0.9rem'}}>
                  {nft.description}
                </Card.Text>
                <div className="mb-3">
                  <small style={{color: '#9ca3af'}}>
                    Seller: {formatAddress(nft.seller)}
                  </small>
                </div>
                <Button
                  variant="primary"
                  className="w-100"
                  onClick={() => buyNFT(nft.tokenId, nft.price)}
                  disabled={!account || loading}
                >
                  {loading ? 'Processing...' : 'Buy Now'}
                </Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      {nfts.length === 0 && !loading && (
        <Row className="justify-content-center mt-5">
          <Col md={6}>
            <Alert variant="light" className="text-center border">
              <h5 style={{color: '#1f2937'}}>No NFTs available</h5>
              <p style={{color: '#6b7280'}}>Check back later for new listings</p>
            </Alert>
          </Col>
        </Row>
      )}
    </Container>
  );
};

export default Marketplace;