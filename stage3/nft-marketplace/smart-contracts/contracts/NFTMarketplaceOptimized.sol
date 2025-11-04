// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title NFTMarketplace - Gas Optimized Version
 * @notice Optimizations applied:
 * 1. Packed struct (uint96 for price, saves 1 storage slot)
 * 2. Cached storage reads in memory
 * 3. Unchecked arithmetic where overflow impossible
 * 4. Minimize SSTORE operations
 * 5. Early returns to save gas on reverts
 */
contract NFTMarketplace is ERC721, ERC721URIStorage, Ownable, ReentrancyGuard {
    // Optimization 1: Pack struct into single slot (32 bytes)
    // uint96 = 12 bytes (enough for price up to ~79 billion ETH)
    // address = 20 bytes
    // Total = 32 bytes = 1 storage slot (saves 1 SSTORE = ~20k gas)
    struct Listing {
        uint96 price;      // 12 bytes
        address seller;    // 20 bytes
        // isActive removed, use price > 0 instead
    }

    mapping(uint256 => Listing) public listings;
    mapping(address => uint256) public pendingWithdrawals;

    uint256 private nextTokenIdCounter;
    uint96 public listingFee = 0.01 ether; // Use uint96 instead of uint256

    event NFTListed(uint256 indexed tokenId, address indexed seller, uint256 price);
    event NFTSold(uint256 indexed tokenId, address indexed buyer, address indexed seller, uint256 price);
    event ListingCancelled(uint256 indexed tokenId);
    event ListingFeeUpdated(uint256 newFee);

    constructor() ERC721("NFT Marketplace", "NFTM") Ownable(msg.sender) {}

    function mintNFT(string memory uri) external returns (uint256) {
        uint256 tokenId;
        // Optimization 2: Use unchecked for counter (no overflow risk in practice)
        unchecked {
            tokenId = nextTokenIdCounter++;
        }
        _mint(msg.sender, tokenId);
        _setTokenURI(tokenId, uri);
        return tokenId;
    }

    function listNFT(uint256 tokenId, uint256 price) external payable nonReentrant {
        // Optimization 3: Early validation before storage reads
        require(price > 0, "Price must be greater than 0");
        require(price <= type(uint96).max, "Price too high");
        require(msg.value >= listingFee, "Insufficient listing fee");
        
        require(ownerOf(tokenId) == msg.sender, "Not the owner");
        
        // Optimization 4: Check if active using price (no need for bool)
        require(listings[tokenId].price == 0, "Already listed");

        // Single SSTORE instead of three
        listings[tokenId] = Listing({
            price: uint96(price),
            seller: msg.sender
        });

        // Optimization 5: Calculate refund once
        uint256 refund;
        unchecked {
            refund = msg.value - listingFee;
        }

        // Transfer listing fee to contract owner
        payable(owner()).transfer(listingFee);

        // Refund excess payment if any
        if (refund > 0) {
            payable(msg.sender).transfer(refund);
        }

        emit NFTListed(tokenId, msg.sender, price);
    }

    function buyNFT(uint256 tokenId) external payable nonReentrant {
        // Optimization 6: Load to memory once (saves multiple SLOADs)
        Listing memory listing = listings[tokenId];
        
        // Early validation
        require(listing.price > 0, "NFT not listed");
        require(msg.value >= listing.price, "Insufficient payment");

        // Optimization 7: Delete listing (SSTORE to 0 = gas refund)
        delete listings[tokenId];

        // Transfer NFT to buyer
        _transfer(listing.seller, msg.sender, tokenId);

        // Optimization 8: Use unchecked for addition (no overflow with ETH amounts)
        unchecked {
            pendingWithdrawals[listing.seller] += listing.price;
        }

        // Calculate and refund excess
        uint256 refund;
        unchecked {
            refund = msg.value - listing.price;
        }
        
        if (refund > 0) {
            payable(msg.sender).transfer(refund);
        }

        emit NFTSold(tokenId, msg.sender, listing.seller, listing.price);
    }

    function cancelListing(uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender, "Not the owner");
        require(listings[tokenId].price > 0, "Not listed");

        // Optimization 9: Delete instead of setting false (gas refund)
        delete listings[tokenId];
        
        emit ListingCancelled(tokenId);
    }

    function withdrawFunds() external nonReentrant {
        // Optimization 10: Cache in memory
        uint256 amount = pendingWithdrawals[msg.sender];
        require(amount > 0, "No funds to withdraw");

        // Reset before transfer (checks-effects-interactions)
        pendingWithdrawals[msg.sender] = 0;
        
        payable(msg.sender).transfer(amount);
    }

    function getListing(uint256 tokenId) external view returns (uint96 price, address seller, bool isActive) {
        Listing memory listing = listings[tokenId];
        return (listing.price, listing.seller, listing.price > 0);
    }

    function getPendingWithdrawal(address seller) external view returns (uint256) {
        return pendingWithdrawals[seller];
    }

    function setListingFee(uint256 newFee) external onlyOwner {
        require(newFee <= type(uint96).max, "Fee too high");
        listingFee = uint96(newFee);
        emit ListingFeeUpdated(newFee);
    }

    // Override functions
    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId) public view override(ERC721, ERC721URIStorage) returns (bool) {
        return super.supportsInterface(interfaceId);
    }

    function _update(address to, uint256 tokenId, address auth) internal override(ERC721) returns (address) {
        address from = _ownerOf(tokenId);
        
        // Optimization 11: Only write if necessary
        if (from != address(0)) {
            Listing memory listing = listings[tokenId];
            if (listing.price > 0) {
                // Cancel listing if NFT is transferred
                delete listings[tokenId];
            }
        }
        
        return super._update(to, tokenId, auth);
    }
}
