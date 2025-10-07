from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

RPC_WSS = os.getenv("RPC_WSS") or os.getenv("RPC_HTTP")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CHAIN_ID = int(os.getenv("CHAIN_ID", 1))

ARBITRAGE_CONTRACT = Web3.toChecksumAddress(os.getenv("ARBITRAGE_CONTRACT"))
UNIV2_PAIR = Web3.toChecksumAddress(os.getenv("UNIV2_PAIR"))
SUSHI_PAIR = Web3.toChecksumAddress(os.getenv("SUSHI_PAIR"))

AMOUNT_IN_ETH = float(os.getenv("AMOUNT_IN_ETH", 0.5))
FEE_RATE = float(os.getenv("FEE_RATE", 0.003))
MIN_PROFIT_ETH = float(os.getenv("MIN_PROFIT_ETH", 0.005))

POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 2))
