import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert, Spinner } from 'react-bootstrap';
import { useWeb3 } from '../context/Web3Context';

const CreateNFT = () => {
  const { contract, account, getContractWithMetaMask, setError, setLoading } = useWeb3();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    imageUrl: ''
  });
  const [minting, setMinting] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const createMetadata = (name, description, imageUrl) => {
    // In a real application, you'd upload to IPFS and get a proper metadata URI
    // For now, we'll create a simple JSON structure and encode it
    const metadata = {
      name,
      description,
      image: imageUrl,
      attributes: []
    };

    // In production, upload to IPFS and return the IPFS URI
    // For demo purposes, we'll use a data URL
    const metadataString = JSON.stringify(metadata);
    const metadataURI = `data:application/json;base64,${btoa(metadataString)}`;

    return metadataURI;
  };

  const mintNFT = async (e) => {
    e.preventDefault();

    try {
      setMinting(true);
      setError('');

      if (!account) {
        throw new Error('Please connect your wallet first');
      }

      if (!formData.name || !formData.description || !formData.imageUrl) {
        throw new Error('Please fill in all fields');
      }

      const contractWithMetaMask = getContractWithMetaMask();
      if (!contractWithMetaMask) {
        throw new Error('Contract not available');
      }

      // Create metadata URI
      const tokenURI = createMetadata(
        formData.name,
        formData.description,
        formData.imageUrl
      );

      // Mint the NFT
      const result = await contractWithMetaMask.methods.mintNFT(tokenURI).send({
        from: account,
        gas: 300000
      });

      // Get the token ID from the transaction receipt
      const tokenId = result.events.Transfer.returnValues.tokenId;

      // Reset form
      setFormData({
        name: '',
        description: '',
        imageUrl: ''
      });

      alert(`NFT minted successfully! Token ID: ${tokenId}`);

    } catch (err) {
      setError('Failed to mint NFT: ' + err.message);
    } finally {
      setMinting(false);
    }
  };

  if (!account) {
    return (
      <Container>
        <Row className="justify-content-center">
          <Col md={6}>
            <Alert variant="warning" className="text-center">
              <h5>Please connect your wallet</h5>
              <p>Connect your wallet to create and mint NFTs</p>
            </Alert>
          </Col>
        </Row>
      </Container>
    );
  }

  return (
    <Container>
      <Row className="justify-content-center">
        <Col lg={8}>
          <Card>
            <Card.Header>
              <h3 className="mb-0">Create New NFT</h3>
            </Card.Header>
            <Card.Body>
              <Form onSubmit={mintNFT}>
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>NFT Name *</Form.Label>
                      <Form.Control
                        type="text"
                        name="name"
                        placeholder="Enter NFT name"
                        value={formData.name}
                        onChange={handleInputChange}
                        required
                      />
                    </Form.Group>

                    <Form.Group className="mb-3">
                      <Form.Label>Description *</Form.Label>
                      <Form.Control
                        as="textarea"
                        rows={3}
                        name="description"
                        placeholder="Describe your NFT"
                        value={formData.description}
                        onChange={handleInputChange}
                        required
                      />
                    </Form.Group>

                    <Form.Group className="mb-3">
                      <Form.Label>Image URL *</Form.Label>
                      <Form.Control
                        type="url"
                        name="imageUrl"
                        placeholder="https://example.com/image.jpg"
                        value={formData.imageUrl}
                        onChange={handleInputChange}
                        required
                      />
                      <Form.Text className="text-muted">
                        Provide a direct link to your NFT image
                      </Form.Text>
                    </Form.Group>
                  </Col>

                  <Col md={6}>
                    <div className="mb-3">
                      <Form.Label>Preview</Form.Label>
                      <div
                        className="border rounded d-flex align-items-center justify-content-center"
                        style={{ height: '300px', backgroundColor: '#f8f9fa' }}
                      >
                        {formData.imageUrl ? (
                          <img
                            src={formData.imageUrl}
                            alt="NFT Preview"
                            className="img-fluid rounded"
                            style={{ maxHeight: '280px' }}
                            onError={(e) => {
                              e.target.src = 'https://via.placeholder.com/300x200/6c757d/ffffff?text=Invalid+Image+URL';
                            }}
                          />
                        ) : (
                          <div className="text-center text-muted">
                            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🖼️</div>
                            <p>Image preview will appear here</p>
                          </div>
                        )}
                      </div>
                    </div>
                  </Col>
                </Row>

                <div className="d-grid">
                  <Button
                    variant="primary"
                    type="submit"
                    size="lg"
                    disabled={minting}
                  >
                    {minting ? (
                      <>
                        <Spinner animation="border" size="sm" className="me-2" />
                        Minting NFT...
                      </>
                    ) : (
                      'Mint NFT'
                    )}
                  </Button>
                </div>
              </Form>

              <Alert variant="info" className="mt-4">
                <strong>Note:</strong> In a production environment, NFT metadata would be uploaded to IPFS for permanent storage. This demo uses inline metadata for simplicity.
              </Alert>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default CreateNFT;