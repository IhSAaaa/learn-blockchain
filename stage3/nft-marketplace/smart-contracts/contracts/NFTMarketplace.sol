// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract NFTMarketplace is ERC721, ERC721URIStorage, Ownable, ReentrancyGuard {
    struct Listing {
        uint256 price;
        address seller;
        bool isActive;
    }

    mapping(uint256 => Listing) public listings;
    mapping(address => uint256) public pendingWithdrawals;

    uint256 private nextTokenIdCounter;
    uint256 public listingFee = 0.01 ether; // Platform fee for listings

    event NFTListed(uint256 indexed tokenId, address indexed seller, uint256 price);
    event NFTSold(uint256 indexed tokenId, address indexed buyer, address indexed seller, uint256 price);
    event ListingCancelled(uint256 indexed tokenId);
    event ListingFeeUpdated(uint256 newFee);

    constructor() ERC721("NFT Marketplace", "NFTM") Ownable(msg.sender) {}

    function mintNFT(string memory uri) external returns (uint256) {
        uint256 tokenId = nextTokenIdCounter++;
        _mint(msg.sender, tokenId);
        _setTokenURI(tokenId, uri);
        return tokenId;
    }

    function listNFT(uint256 tokenId, uint256 price) external payable nonReentrant {
        require(ownerOf(tokenId) == msg.sender, "Not the owner");
        require(price > 0, "Price must be greater than 0");
        require(msg.value >= listingFee, "Insufficient listing fee");
        require(!listings[tokenId].isActive, "Already listed");

        listings[tokenId] = Listing({
            price: price,
            seller: msg.sender,
            isActive: true
        });

        // Transfer listing fee to contract owner
        payable(owner()).transfer(listingFee);

        // Refund excess payment
        if (msg.value > listingFee) {
            payable(msg.sender).transfer(msg.value - listingFee);
        }

        emit NFTListed(tokenId, msg.sender, price);
    }

    function buyNFT(uint256 tokenId) external payable nonReentrant {
        Listing memory listing = listings[tokenId];
        require(listing.isActive, "NFT not listed");
        require(msg.value >= listing.price, "Insufficient payment");

        // Mark listing as inactive
        listings[tokenId].isActive = false;

        // Transfer NFT to buyer
        _transfer(listing.seller, msg.sender, tokenId);

        // Store payment for seller
        pendingWithdrawals[listing.seller] += listing.price;

        // Refund excess payment
        if (msg.value > listing.price) {
            payable(msg.sender).transfer(msg.value - listing.price);
        }

        emit NFTSold(tokenId, msg.sender, listing.seller, listing.price);
    }

    function cancelListing(uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender, "Not the owner");
        require(listings[tokenId].isActive, "Not listed");

        listings[tokenId].isActive = false;
        emit ListingCancelled(tokenId);
    }

    function withdrawFunds() external nonReentrant {
        uint256 amount = pendingWithdrawals[msg.sender];
        require(amount > 0, "No funds to withdraw");

        pendingWithdrawals[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }

    function getListing(uint256 tokenId) external view returns (Listing memory) {
        return listings[tokenId];
    }

    function getPendingWithdrawal(address seller) external view returns (uint256) {
        return pendingWithdrawals[seller];
    }

    function setListingFee(uint256 newFee) external onlyOwner {
        listingFee = newFee;
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
        if (from != address(0) && listings[tokenId].isActive) {
            // Cancel listing if NFT is transferred
            listings[tokenId].isActive = false;
        }
        return super._update(to, tokenId, auth);
    }
}