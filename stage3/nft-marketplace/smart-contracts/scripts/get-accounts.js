const { ethers } = require("hardhat");

async function main() {
  console.log("🔑 Hardhat Local Network Accounts:");
  console.log("=====================================");

  // Get the signers (accounts) from Hardhat
  const accounts = await ethers.getSigners();

  for (let i = 0; i < Math.min(5, accounts.length); i++) {
    const account = accounts[i];
    const address = await account.getAddress();
    const balance = await ethers.provider.getBalance(address);

    console.log(`\nAccount ${i}:`);
    console.log(`Address: ${address}`);
    console.log(`Balance: ${ethers.utils.formatEther(balance)} ETH`);
  }

  console.log("\n📝 Note: These are deterministic accounts for local development.");
  console.log("🚨 Never use these private keys on mainnet or testnets!");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });