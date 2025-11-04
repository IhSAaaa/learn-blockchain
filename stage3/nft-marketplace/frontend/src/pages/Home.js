import React from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { useWeb3 } from '../context/Web3Context';

const Home = () => {
  const { account, switchToLocalNetwork, networkId } = useWeb3();

  return (
    <Container className="py-5">
      <Row className="mb-5">
        <Col lg={8} className="mx-auto text-center">
          <h1 className="mb-3" style={{color: '#1f2937', fontWeight: '600', fontSize: '2.5rem'}}>
            NFT Marketplace
          </h1>
          <p className="mb-4" style={{color: '#6b7280', fontSize: '1.1rem'}}>
            Buy, sell, and discover unique digital assets
          </p>

          {!account && (
            <div className="alert alert-light border" style={{background: '#fef3c7', borderColor: '#fbbf24'}}>
              <strong>Get Started:</strong> Connect your wallet to explore the marketplace
            </div>
          )}

          {account && networkId !== 1337 && (
            <div className="alert alert-light border" style={{background: '#fef3c7', borderColor: '#fbbf24'}}>
              <strong>Network:</strong> Switch to Localhost 8545 to use the marketplace
              <br />
              <Button
                variant="outline-primary"
                size="sm"
                className="mt-2"
                onClick={switchToLocalNetwork}
              >
                Switch Network
              </Button>
            </div>
          )}
        </Col>
      </Row>

      <Row className="g-4 mb-5">
        <Col md={4}>
          <Card className="h-100 border">
            <Card.Body className="text-center p-4">
              <div className="mb-3" style={{fontSize: '2.5rem'}}>✏️</div>
              <Card.Title style={{color: '#1f2937', fontSize: '1.25rem', fontWeight: '600'}}>
                Create NFTs
              </Card.Title>
              <Card.Text style={{color: '#6b7280'}}>
                Mint your digital assets with custom metadata
              </Card.Text>
              <LinkContainer to="/create">
                <Button variant="primary" className="mt-2">Create</Button>
              </LinkContainer>
            </Card.Body>
          </Card>
        </Col>

        <Col md={4}>
          <Card className="h-100 border">
            <Card.Body className="text-center p-4">
              <div className="mb-3" style={{fontSize: '2.5rem'}}>�</div>
              <Card.Title style={{color: '#1f2937', fontSize: '1.25rem', fontWeight: '600'}}>
                Explore Market
              </Card.Title>
              <Card.Text style={{color: '#6b7280'}}>
                Browse and purchase NFTs from creators
              </Card.Text>
              <LinkContainer to="/marketplace">
                <Button variant="primary" className="mt-2">Explore</Button>
              </LinkContainer>
            </Card.Body>
          </Card>
        </Col>

        <Col md={4}>
          <Card className="h-100 border">
            <Card.Body className="text-center p-4">
              <div className="mb-3" style={{fontSize: '2.5rem'}}>�</div>
              <Card.Title style={{color: '#1f2937', fontSize: '1.25rem', fontWeight: '600'}}>
                Your Collection
              </Card.Title>
              <Card.Text style={{color: '#6b7280'}}>
                Manage your NFTs and track your portfolio
              </Card.Text>
              <LinkContainer to="/my-nfts">
                <Button variant="primary" className="mt-2">View NFTs</Button>
              </LinkContainer>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row>
        <Col lg={10} className="mx-auto">
          <Card className="border" style={{background: '#f9fafb'}}>
            <Card.Body className="p-4">
              <h4 className="text-center mb-4" style={{color: '#1f2937', fontWeight: '600'}}>
                How It Works
              </h4>
              <Row className="g-4">
                <Col md={3} className="text-center">
                  <div className="mb-3">
                    <div className="d-inline-flex align-items-center justify-content-center" 
                         style={{width: '48px', height: '48px', background: '#e5e7eb', borderRadius: '50%', color: '#374151', fontWeight: '600'}}>
                      1
                    </div>
                  </div>
                  <h6 style={{color: '#1f2937', fontWeight: '600'}}>Connect</h6>
                  <p className="small" style={{color: '#6b7280'}}>
                    Link your wallet
                  </p>
                </Col>
                <Col md={3} className="text-center">
                  <div className="mb-3">
                    <div className="d-inline-flex align-items-center justify-content-center" 
                         style={{width: '48px', height: '48px', background: '#e5e7eb', borderRadius: '50%', color: '#374151', fontWeight: '600'}}>
                      2
                    </div>
                  </div>
                  <h6 style={{color: '#1f2937', fontWeight: '600'}}>Create or Browse</h6>
                  <p className="small" style={{color: '#6b7280'}}>
                    Mint or explore NFTs
                  </p>
                </Col>
                <Col md={3} className="text-center">
                  <div className="mb-3">
                    <div className="d-inline-flex align-items-center justify-content-center" 
                         style={{width: '48px', height: '48px', background: '#e5e7eb', borderRadius: '50%', color: '#374151', fontWeight: '600'}}>
                      3
                    </div>
                  </div>
                  <h6 style={{color: '#1f2937', fontWeight: '600'}}>List</h6>
                  <p className="small" style={{color: '#6b7280'}}>
                    Set your price
                  </p>
                </Col>
                <Col md={3} className="text-center">
                  <div className="mb-3">
                    <div className="d-inline-flex align-items-center justify-content-center" 
                         style={{width: '48px', height: '48px', background: '#e5e7eb', borderRadius: '50%', color: '#374151', fontWeight: '600'}}>
                      4
                    </div>
                  </div>
                  <h6 style={{color: '#1f2937', fontWeight: '600'}}>Trade</h6>
                  <p className="small" style={{color: '#6b7280'}}>
                    Buy and sell securely
                  </p>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Home;