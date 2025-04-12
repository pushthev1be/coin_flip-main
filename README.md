# 🪙 Crypto Coin Flip 🎲

A simple and fun decentralized app (dApp) that lets users flip a coin using their Solana wallet (e.g. Phantom) and potentially double their crypto! Built using HTML, Bootstrap, and Solana Web3 tools.

## 🚀 Features

- 🔐 **Connect Solana Wallet:** Supports Phantom for secure wallet connection.
- 💰 **Wager SOL:** Users can specify the amount of SOL they want to bet.
- 🪙 **Heads or Tails Flip:** Randomly determines outcome (can be modified server-side for provable fairness).
- 📈 **Live Flip Feed:** Real-time updates of recent coin flips with outcomes and profits.
- 🎨 **Tiled Background + UI Enhancements:** Uses a tiled Nike-themed crypto background and stylish Bootstrap/Montserrat UI.

## 🧱 Built With

- Frontend: `HTML`, `CSS`, `Bootstrap 5`, `JavaScript`
- Web3 Integration: `Phantom Wallet`, `Solana JavaScript API`
- Backend: (Expected to be connected)
  - `Node.js` server with endpoints `/flip` and `/recent-flips`
  - Logic to process coin flip outcome and manage wagered funds

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/crypto-coin-flip.git
cd crypto-coin-flip

2. Run the Backend (Assumed)
Make sure your Node.js backend is running and has the following POST and GET endpoints:

POST /flip — handles coin flip logic and returns outcome.

GET /recent-flips — returns a list of recent flips.

Example command (if backend exists in server/ folder):

bash
Copy
Edit
cd server
npm install
npm start
3. Open the Frontend
Simply open the index.html file in your browser or host it on a static web server:

bash
Copy
Edit
open index.html
Or use Live Server in VS Code.
