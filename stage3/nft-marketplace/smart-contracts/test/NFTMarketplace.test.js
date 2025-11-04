const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("NFTMarketplace", function () {
  let nftMarketplace;
  let owner, seller, buyer, otherAccount;
  let tokenURI = "https://example.com/nft/1";

  beforeEach(async function () {
    [owner, seller, buyer, otherAccount] = await ethers.getSigners();

    const NFTMarketplace = await ethers.getContractFactory("NFTMarketplace");
    nftMarketplace = await NFTMarketplace.deploy();
    await nftMarketplace.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      expect(await nftMarketplace.owner()).to.equal(owner.address);
    });

    it("Should have correct name and symbol", async function () {
      expect(await nftMarketplace.name()).to.equal("NFT Marketplace");
      expect(await nftMarketplace.symbol()).to.equal("NFTM");
    });
  });

  describe("Minting", function () {
    it("Should mint NFT and assign to caller", async function () {
      await nftMarketplace.connect(seller).mintNFT(tokenURI);
      expect(await nftMarketplace.ownerOf(0)).to.equal(seller.address);
      expect(await nftMarketplace.tokenURI(0)).to.equal(tokenURI);
    });

    it("Should increment token ID for each mint", async function () {
      await nftMarketplace.connect(seller).mintNFT(tokenURI);
      await nftMarketplace.connect(seller).mintNFT(tokenURI + "2");

      expect(await nftMarketplace.ownerOf(0)).to.equal(seller.address);
      expect(await nftMarketplace.ownerOf(1)).to.equal(seller.address);
    });
  });

  describe("Listing", function () {
    const price = ethers.parseEther("1");
    const listingFee = ethers.parseEther("0.01");

    beforeEach(async function () {
      await nftMarketplace.connect(seller).mintNFT(tokenURI);
    });

    it("Should list NFT for sale", async function () {
      await expect(
        nftMarketplace.connect(seller).listNFT(0, price, { value: listingFee })
      )
        .to.emit(nftMarketplace, "NFTListed")
        .withArgs(0, seller.address, price);

      const listing = await nftMarketplace.getListing(0);
      expect(listing.price).to.equal(price);
      expect(listing.seller).to.equal(seller.address);
      expect(listing.isActive).to.equal(true);
    });

    it("Should reject listing without sufficient fee", async function () {
      await expect(
        nftMarketplace.connect(seller).listNFT(0, price, { value: ethers.parseEther("0.005") })
      ).to.be.revertedWith("Insufficient listing fee");
    });

    it("Should reject listing by non-owner", async function () {
      await expect(
        nftMarketplace.connect(buyer).listNFT(0, price, { value: listingFee })
      ).to.be.revertedWith("Not the owner");
    });

    it("Should reject listing already listed NFT", async function () {
      await nftMarketplace.connect(seller).listNFT(0, price, { value: listingFee });
      await expect(
        nftMarketplace.connect(seller).listNFT(0, price, { value: listingFee })
      ).to.be.revertedWith("Already listed");
    });

    it("Should refund excess listing fee", async function () {
      const excessFee = ethers.parseEther("0.02");
      const initialBalance = await ethers.provider.getBalance(seller.address);

      await nftMarketplace.connect(seller).listNFT(0, price, { value: excessFee });

      const finalBalance = await ethers.provider.getBalance(seller.address);
      // Should have spent exactly the listing fee
      expect(initialBalance - finalBalance).to.be.closeTo(listingFee, ethers.parseEther("0.001"));
    });
  });

  describe("Buying", function () {
    const price = ethers.parseEther("1");
    const listingFee = ethers.parseEther("0.01");

    beforeEach(async function () {
      await nftMarketplace.connect(seller).mintNFT(tokenURI);
      await nftMarketplace.connect(seller).listNFT(0, price, { value: listingFee });
    });

    it("Should buy NFT and transfer ownership", async function () {
      await expect(
        nftMarketplace.connect(buyer).buyNFT(0, { value: price })
      )
        .to.emit(nftMarketplace, "NFTSold")
        .withArgs(0, buyer.address, seller.address, price);

      expect(await nftMarketplace.ownerOf(0)).to.equal(buyer.address);
      expect((await nftMarketplace.getListing(0)).isActive).to.equal(false);
    });

    it("Should store payment for seller withdrawal", async function () {
      await nftMarketplace.connect(buyer).buyNFT(0, { value: price });

      expect(await nftMarketplace.getPendingWithdrawal(seller.address)).to.equal(price);
    });

    it("Should reject buying unlisted NFT", async function () {
      await nftMarketplace.connect(seller).cancelListing(0);
      await expect(
        nftMarketplace.connect(buyer).buyNFT(0, { value: price })
      ).to.be.revertedWith("NFT not listed");
    });

    it("Should reject insufficient payment", async function () {
      await expect(
        nftMarketplace.connect(buyer).buyNFT(0, { value: ethers.parseEther("0.5") })
      ).to.be.revertedWith("Insufficient payment");
    });

    it("Should refund excess payment", async function () {
      const excessPayment = ethers.parseEther("1.5");
      const initialBalance = await ethers.provider.getBalance(buyer.address);

      await nftMarketplace.connect(buyer).buyNFT(0, { value: excessPayment });

      const finalBalance = await ethers.provider.getBalance(buyer.address);
      // Should have spent exactly the price
      expect(initialBalance - finalBalance).to.be.closeTo(price, ethers.parseEther("0.001"));
    });
  });

  describe("Cancelling Listings", function () {
    const price = ethers.parseEther("1");
    const listingFee = ethers.parseEther("0.01");

    beforeEach(async function () {
      await nftMarketplace.connect(seller).mintNFT(tokenURI);
      await nftMarketplace.connect(seller).listNFT(0, price, { value: listingFee });
    });

    it("Should cancel listing", async function () {
      await expect(nftMarketplace.connect(seller).cancelListing(0))
        .to.emit(nftMarketplace, "ListingCancelled")
        .withArgs(0);

      expect((await nftMarketplace.getListing(0)).isActive).to.equal(false);
    });

    it("Should reject cancelling by non-owner", async function () {
      await expect(
        nftMarketplace.connect(buyer).cancelListing(0)
      ).to.be.revertedWith("Not the owner");
    });

    it("Should reject cancelling unlisted NFT", async function () {
      await nftMarketplace.connect(seller).cancelListing(0);
      await expect(
        nftMarketplace.connect(seller).cancelListing(0)
      ).to.be.revertedWith("Not listed");
    });
  });

  describe("Withdrawals", function () {
    const price = ethers.parseEther("1");
    const listingFee = ethers.parseEther("0.01");

    beforeEach(async function () {
      await nftMarketplace.connect(seller).mintNFT(tokenURI);
      await nftMarketplace.connect(seller).listNFT(0, price, { value: listingFee });
      await nftMarketplace.connect(buyer).buyNFT(0, { value: price });
    });

    it("Should withdraw pending funds", async function () {
      const initialBalance = await ethers.provider.getBalance(seller.address);

      await nftMarketplace.connect(seller).withdrawFunds();

      const finalBalance = await ethers.provider.getBalance(seller.address);
      expect(finalBalance - initialBalance).to.be.closeTo(price, ethers.parseEther("0.001"));
      expect(await nftMarketplace.getPendingWithdrawal(seller.address)).to.equal(0);
    });

    it("Should reject withdrawal with no funds", async function () {
      await nftMarketplace.connect(seller).withdrawFunds(); // First withdrawal succeeds
      await expect(
        nftMarketplace.connect(seller).withdrawFunds()
      ).to.be.revertedWith("No funds to withdraw");
    });
  });

  describe("Admin Functions", function () {
    it("Should update listing fee", async function () {
      const newFee = ethers.parseEther("0.02");

      await expect(nftMarketplace.connect(owner).setListingFee(newFee))
        .to.emit(nftMarketplace, "ListingFeeUpdated")
        .withArgs(newFee);

      expect(await nftMarketplace.listingFee()).to.equal(newFee);
    });

    it("Should reject listing fee update by non-owner", async function () {
      await expect(
        nftMarketplace.connect(seller).setListingFee(ethers.parseEther("0.02"))
      ).to.be.revertedWithCustomError(nftMarketplace, "OwnableUnauthorizedAccount");
    });
  });

  describe("Transfer Behavior", function () {
    const price = ethers.parseEther("1");
    const listingFee = ethers.parseEther("0.01");

    it("Should cancel listing when NFT is transferred", async function () {
      await nftMarketplace.connect(seller).mintNFT(tokenURI);
      await nftMarketplace.connect(seller).listNFT(0, price, { value: listingFee });

      await nftMarketplace.connect(seller).transferFrom(seller.address, buyer.address, 0);

      expect((await nftMarketplace.getListing(0)).isActive).to.equal(false);
    });
  });
});