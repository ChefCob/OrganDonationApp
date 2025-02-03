🚀 README Guide: How to Deploy & Execute the Organ Donation Website
📌 Project Overview
This project is a secure organ donation matching system that:
✅ Matches donors & recipients based on medical criteria.
✅ Uses blockchain (Ethereum) to store matches securely.
✅ Has a Flask backend & Web3.js frontend for interaction.
🛠️ Step 1: Clone the Repository
git clone https://github.com/YOUR-USERNAME/OrganDonationApp.git
cd OrganDonationApp
🖥️ Step 2: Set Up the Backend (Flask)
1️⃣ Install Python & Virtual Environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
2️⃣ Start the Flask Server
python app.py
The backend should now run at http://127.0.0.1:5000/.
🌐 Step 3: Run the Frontend
1️⃣ Start a Local Server
python -m http.server 8000
⛓️ Step 4: Set Up & Deploy the Blockchain Smart Contract
1️⃣ Install Node.js & Hardhat
npm install -g npm
npm install --save-dev hardhat
npx hardhat
Select "Create a JavaScript project".
2️⃣ Start a Local Blockchain
npx hardhat node
3️⃣ Deploy the Smart Contract
npx hardhat run scripts/deploy.js --network localhost
Step 5: Connect Frontend to Blockchain
1️⃣ Update index.html
Open index.html and replace contractAddress with the copied address.
2️⃣ Open MetaMask & Connect to Localhost
Open MetaMask, go to Settings → Networks → Add Network.
Set RPC URL to: http://127.0.0.1:8545/.
Final Step: Test the System
1️⃣ Register a Donor & Recipient
Open http://127.0.0.1:8000/index.html
Fill in donor & recipient details.
Click Submit Donor and Submit Recipient.
2️⃣ Find a Match
Click "Find Match".
MetaMask will pop up → Confirm the transaction.
The match will be stored on the blockchain.
🎯 Summary
✅ Clone & Set Up Flask Backend
✅ Run Local Frontend Server
✅ Deploy Smart Contract & Connect MetaMask
✅ Register & Match Donors Securely

