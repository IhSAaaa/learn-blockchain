import React from 'react';
import { Navbar, Nav, Container, Button, Badge } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { useWeb3 } from '../context/Web3Context';

const Header = () => {
  const { account, connectWallet, disconnectWallet, loading } = useWeb3();

  const formatAddress = (address) => {
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  };

  return (
    <Navbar bg="white" expand="lg" className="border-bottom shadow-sm">
      <Container>
        <LinkContainer to="/">
          <Navbar.Brand className="fw-semibold" style={{color: '#1f2937'}}>
            NFT Market
          </Navbar.Brand>
        </LinkContainer>

        <Navbar.Toggle aria-controls="basic-navbar-nav" />

        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <LinkContainer to="/marketplace">
              <Nav.Link style={{color: '#4b5563'}}>Marketplace</Nav.Link>
            </LinkContainer>
            <LinkContainer to="/my-nfts">
              <Nav.Link style={{color: '#4b5563'}}>My NFTs</Nav.Link>
            </LinkContainer>
            <LinkContainer to="/create">
              <Nav.Link style={{color: '#4b5563'}}>Create</Nav.Link>
            </LinkContainer>
          </Nav>

          <Nav>
            {account ? (
              <div className="d-flex align-items-center gap-2">
                <span className="wallet-address">
                  {formatAddress(account)}
                </span>
                <Button
                  variant="outline-secondary"
                  size="sm"
                  onClick={disconnectWallet}
                >
                  Disconnect
                </Button>
              </div>
            ) : (
              <Button
                variant="primary"
                size="sm"
                onClick={connectWallet}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="loading-spinner me-2"></span>
                    Connecting...
                  </>
                ) : (
                  'Connect Wallet'
                )}
              </Button>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;