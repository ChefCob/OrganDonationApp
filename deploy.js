const hre = require("hardhat");

async function main() {
    // Deploy the contract
    const OrganDonation = await hre.ethers.deployContract("OrganDonation");

    console.log(`✅ Contract deployed to: ${await OrganDonation.getAddress()}`);
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
