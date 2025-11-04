const { ethers } = require("hardhat");

async function main() {
  console.log("Deploying NFT Marketplace contract...");

  // Get the contract factory
  const NFTMarketplace = await ethers.getContractFactory("NFTMarketplace");

  // Deploy the contract
  const nftMarketplace = await NFTMarketplace.deploy();

  // Wait for deployment to complete
  await nftMarketplace.waitForDeployment();

  const contractAddress = await nftMarketplace.getAddress();
  console.log("NFT Marketplace deployed to:", contractAddress);

  // Verify contract on Etherscan if on a public network
  if (network.name !== "hardhat" && network.name !== "localhost") {
    console.log("Waiting for block confirmations...");
    await nftMarketplace.deploymentTransaction().wait(6);

    console.log("Verifying contract on Etherscan...");
    try {
      await hre.run("verify:verify", {
        address: contractAddress,
        constructorArguments: [],
      });
      console.log("Contract verified successfully!");
    } catch (error) {
      console.log("Verification failed:", error.message);
    }
  }

  // Log deployment info
  console.log("\nDeployment Summary:");
  console.log("===================");
  console.log(`Contract Address: ${contractAddress}`);
  console.log(`Network: ${network.name}`);
  console.log(`Block Number: ${await ethers.provider.getBlockNumber()}`);

  return contractAddress;
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });