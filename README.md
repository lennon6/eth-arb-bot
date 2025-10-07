# ETH Arbitrage Bot

A high-frequency trading bot that identifies and executes profitable arbitrage opportunities between Uniswap V2 and SushiSwap DEXs on the Ethereum network.

## Overview

This bot monitors price differences for token pairs between Uniswap V2 and SushiSwap decentralized exchanges. When it detects a profitable arbitrage opportunity (after accounting for gas fees), it automatically executes trades to capture the price difference.

The bot operates by:
1. Monitoring token reserves on both DEXs in real-time
2. Calculating potential profits from price discrepancies
3. Executing trades when the profit exceeds the configured minimum threshold
4. Handling all transactions through a smart contract for optimal execution

## Features

- Real-time monitoring of Uniswap V2 and SushiSwap liquidity pools
- Configurable trade amounts and profit thresholds
- Gas-optimized smart contract execution
- Support for WETH and UNI token pairs (easily extensible to other tokens)
- Environment-based configuration
- Pure Python implementation with py-solc-x for contract compilation

## Prerequisites

- Python 3.8+
- Web3.py
- py-solc-x (for Solidity compilation)
- An Ethereum node (Infura, Alchemy, or self-hosted)
- Private key with ETH for gas fees

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/eth-arb-bot.git
   cd eth-arb-bot
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r bot/requirements.txt
   ```

3. The Solidity compiler will be automatically installed when you run the deployment script.

## Configuration

1. Create a `.env` file in the root directory with your configuration:
   ```
   # Required
   PRIVATE_KEY=your_private_key_here
   RPC_HTTP=https://your-ethereum-node-http
   RPC_WSS=wss://your-ethereum-node-wss
   
   # Contract addresses (update after deployment)
   ARBITRAGE_CONTRACT=0x...
   UNIV2_PAIR=0x...
   SUSHI_PAIR=0x...
   
   # Trading parameters
   AMOUNT_IN_ETH=0.5
   MIN_PROFIT_ETH=0.005
   FEE_RATE=0.003  # 0.3% fee
   
   # Network settings
   CHAIN_ID=1  # 1 for Mainnet, 5 for Goerli, etc.
   POLL_INTERVAL=2  # seconds between checks
   ```

## Deployment

1. Deploy the smart contract using the Python deployment script:
   ```bash
   python scripts/deploy_contract.py
   ```

2. The script will:
   - Compile the Solidity contract using py-solc-x
   - Deploy it to the network specified in your `.env`
   - Output the deployed contract address

3. Update your `.env` file with the `ARBITRAGE_CONTRACT` address from the deployment output

## Usage

Start the bot:
```bash
python bot/main.py
```

The bot will run continuously, monitoring for arbitrage opportunities and executing trades when profitable.

## Project Structure

```
eth-arb-bot/
├── bot/
│   ├── main.py          # Main bot logic
│   ├── utils.py         # Utility functions for calculations
│   ├── config.py        # Configuration loader
│   └── requirements.txt # Python dependencies
├── contracts/
│   └── ArbExecutor.sol  # Smart contract for arbitrage execution
├── scripts/
│   └── deploy_contract.py  # Contract deployment script
└── .env                 # Environment configuration
```

## How It Works

1. **Monitoring**: The bot continuously polls Uniswap V2 and SushiSwap pair contracts to get current reserves
2. **Calculation**: Uses the constant product formula (x * y = k) to calculate expected output amounts
3. **Profit Check**: Compares the final ETH amount after both swaps against the initial amount plus minimum profit threshold
4. **Execution**: When profitable, calls the `swap()` function on the deployed smart contract which executes both trades atomically

## Security Considerations

- **Never share your private key**
- Start with small trade amounts to test
- Monitor gas prices as they can significantly impact profitability
- The contract executes trades atomically to prevent partial execution
- Test on a testnet (Goerli, Sepolia) before using on mainnet

## License

MIT

## Disclaimer

This software is for educational purposes only. Use at your own risk. The developers are not responsible for any financial losses incurred while using this bot. Always do your own research and understand the risks involved in decentralized finance and arbitrage trading.
