import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Badge, Alert, Spinner, Modal, Form } from 'react-bootstrap';
import { useWeb3 } from '../context/Web3Context';

const MyNFTs = () => {
  const { contract, account, getContractWithMetaMask, setError, setLoading } = useWeb3();
  const [nfts, setNfts] = useState([]);
  const [listings, setListings] = useState({});
  const [loading, setLoadingState] = useState(false);
  const [showListModal, setShowListModal] = useState(false);
  const [selectedNFT, setSelectedNFT] = useState(null);
  const [listingPrice, setListingPrice] = useState('');
  const [pendingWithdrawal, setPendingWithdrawal] = useState('0');

  useEffect(() => {
    if (contract && account) {
      loadUserNFTs();
      loadPendingWithdrawal();
    }
  }, [contract, account]);

  const loadUserNFTs = async () => {
    try {
      setLoadingState(true);
      setError('');

      // In a real implementation, you'd query the user's token balance and iterate through their tokens
      // For now, we'll simulate with mock data
      const mockNFTs = [
        {
          tokenId: 0,
          tokenURI: 'https://via.placeholder.com/300x250/FF6B6B/FFFFFF?text=My+NFT+1',
          name: 'My Cosmic Dream #1',
          description: 'My beautiful cosmic dream artwork',
          owner: account
        },
        {
          tokenId: 1,
          tokenURI: 'https://via.placeholder.com/300x250/4ECDC4/FFFFFF?text=My+NFT+2',
          name: 'My Digital Landscape #2',
          description: 'My stunning digital landscape',
          owner: account
        }
      ];

      setNfts(mockNFTs);

      // Load listing status for each NFT
      const listingStatuses = {};
      for (const nft of mockNFTs) {
        try {
          const listing = await contract.methods.getListing(nft.tokenId).call();
          listingStatuses[nft.tokenId] = listing;
        } catch (err) {
          console.log(`Failed to load listing for token ${nft.tokenId}:`, err);
        }
      }
      setListings(listingStatuses);
    } catch (err) {
      setError('Failed to load your NFTs: ' + err.message);
    } finally {
      setLoadingState(false);
    }
  };

  const loadPendingWithdrawal = async () => {
    try {
      if (contract && account) {
        const amount = await contract.methods.getPendingWithdrawal(account).call();
        setPendingWithdrawal(contract.methods.web3.utils.fromWei(amount, 'ether'));
      }
    } catch (err) {
      console.log('Failed to load pending withdrawal:', err);
    }
  };

  const handleListNFT = (nft) => {
    setSelectedNFT(nft);
    setShowListModal(true);
  };

  const submitListing = async () => {
    try {
      setLoading(true);
      setError('');

      if (!selectedNFT || !listingPrice) {
        throw new Error('Please provide a listing price');
      }

      const contractWithMetaMask = getContractWithMetaMask();
      if (!contractWithMetaMask) {
        throw new Error('Contract not available');
      }

      const priceInWei = contract.methods.web3.utils.toWei(listingPrice, 'ether');
      const listingFee = await contract.methods.listingFee().call();

      await contractWithMetaMask.methods.listNFT(selectedNFT.tokenId, priceInWei).send({
        from: account,
        value: listingFee,
        gas: 300000
      });

      setShowListModal(false);
      setListingPrice('');
      setSelectedNFT(null);

      // Reload NFTs to show updated listing status
      await loadUserNFTs();

      alert('NFT listed successfully!');
    } catch (err) {
      setError('Failed to list NFT: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const cancelListing = async (tokenId) => {
    try {
      setLoading(true);
      setError('');

      const contractWithMetaMask = getContractWithMetaMask();
      if (!contractWithMetaMask) {
        throw new Error('Contract not available');
      }

      await contractWithMetaMask.methods.cancelListing(tokenId).send({
        from: account,
        gas: 200000
      });

      // Reload NFTs to show updated listing status
      await loadUserNFTs();

      alert('Listing cancelled successfully!');
    } catch (err) {
      setError('Failed to cancel listing: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const withdrawFunds = async () => {
    try {
      setLoading(true);
      setError('');

      const contractWithMetaMask = getContractWithMetaMask();
      if (!contractWithMetaMask) {
        throw new Error('Contract not available');
      }

      await contractWithMetaMask.methods.withdrawFunds().send({
        from: account,
        gas: 200000
      });

      setPendingWithdrawal('0');
      alert('Funds withdrawn successfully!');
    } catch (err) {
      setError('Failed to withdraw funds: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!account) {
    return (
      <Container>
        <Row className="justify-content-center">
          <Col md={6}>
            <Alert variant="warning" className="text-center">
              <h5>Please connect your wallet</h5>
              <p>Connect your wallet to view and manage your NFTs</p>
            </Alert>
          </Col>
        </Row>
      </Container>
    );
  }

  return (
    <Container>
      <Row className="mb-4">
        <Col>
          <h2 className="text-white">My NFT Collection</h2>
          <p className="text-white-50">Manage your NFTs and listings</p>
        </Col>
        {parseFloat(pendingWithdrawal) > 0 && (
          <Col xs="auto">
            <Alert variant="success">
              <div className="d-flex justify-content-between align-items-center">
                <span>Pending withdrawal: {pendingWithdrawal} ETH</span>
                <Button
                  variant="outline-success"
                  size="sm"
                  onClick={withdrawFunds}
                  disabled={loading}
                >
                  Withdraw
                </Button>
              </div>
            </Alert>
          </Col>
        )}
      </Row>

      {loading && (
        <Row className="justify-content-center mb-4">
          <Col xs="auto">
            <Spinner animation="border" variant="primary" />
            <span className="ms-2 text-white">Loading your NFTs...</span>
          </Col>
        </Row>
      )}

      <div className="marketplace-grid">
        {nfts.map((nft) => {
          const listing = listings[nft.tokenId];
          const isListed = listing && listing.isActive;

          return (
            <Card key={nft.tokenId} className="nft-card">
              <Card.Img
                variant="top"
                src={nft.tokenURI}
                className="nft-image"
                alt={nft.name}
              />
              <Card.Body>
                <Card.Title className="d-flex justify-content-between align-items-start">
                  <span>{nft.name}</span>
                  {isListed && (
                    <Badge bg="success">Listed</Badge>
                  )}
                </Card.Title>
                <Card.Text className="text-muted small">
                  {nft.description}
                </Card.Text>
                {isListed && (
                  <div className="mb-3">
                    <Badge bg="info">
                      Price: {contract ? contract.methods.web3.utils.fromWei(listing.price, 'ether') : '0'} ETH
                    </Badge>
                  </div>
                )}
                <div className="d-grid gap-2">
                  {!isListed ? (
                    <Button
                      variant="primary"
                      onClick={() => handleListNFT(nft)}
                      disabled={loading}
                    >
                      List for Sale
                    </Button>
                  ) : (
                    <Button
                      variant="outline-danger"
                      onClick={() => cancelListing(nft.tokenId)}
                      disabled={loading}
                    >
                      Cancel Listing
                    </Button>
                  )}
                </div>
              </Card.Body>
            </Card>
          );
        })}
      </div>

      {nfts.length === 0 && !loading && (
        <Row className="justify-content-center">
          <Col md={6}>
            <Alert variant="info" className="text-center">
              <h5>No NFTs found</h5>
              <p>You haven't minted any NFTs yet. Create your first NFT!</p>
            </Alert>
          </Col>
        </Row>
      )}

      {/* List NFT Modal */}
      <Modal show={showListModal} onHide={() => setShowListModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>List NFT for Sale</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedNFT && (
            <div className="mb-3">
              <img
                src={selectedNFT.tokenURI}
                alt={selectedNFT.name}
                className="img-fluid rounded mb-3"
                style={{ maxHeight: '200px' }}
              />
              <h5>{selectedNFT.name}</h5>
              <p className="text-muted">{selectedNFT.description}</p>
            </div>
          )}
          <Form.Group>
            <Form.Label>Listing Price (ETH)</Form.Label>
            <Form.Control
              type="number"
              step="0.01"
              min="0"
              placeholder="0.00"
              value={listingPrice}
              onChange={(e) => setListingPrice(e.target.value)}
            />
            <Form.Text className="text-muted">
              Plus listing fee: 0.01 ETH
            </Form.Text>
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowListModal(false)}>
            Cancel
          </Button>
          <Button
            variant="primary"
            onClick={submitListing}
            disabled={!listingPrice || loading}
          >
            {loading ? 'Listing...' : 'List NFT'}
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default MyNFTs;