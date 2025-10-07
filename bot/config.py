from web3 import Web3
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def get_required_env(key):
    """Get required environment variable or exit with error message."""
    value = os.getenv(key)
    if not value:
        print(f"ERROR: Missing required environment variable: {key}")
        print(f"Please add {key} to your .env file")
        sys.exit(1)
    return value

RPC_WSS = get_required_env("RPC_WSS") if os.getenv("RPC_WSS") else os.getenv("RPC_HTTP")
if not RPC_WSS:
    print("ERROR: Either RPC_WSS or RPC_HTTP must be set in .env")
    sys.exit(1)

PRIVATE_KEY = get_required_env("PRIVATE_KEY")
CHAIN_ID = int(os.getenv("CHAIN_ID", 1))

ARBITRAGE_CONTRACT = Web3.toChecksumAddress(get_required_env("ARBITRAGE_CONTRACT"))
UNIV2_PAIR = Web3.toChecksumAddress(get_required_env("UNIV2_PAIR"))
SUSHI_PAIR = Web3.toChecksumAddress(get_required_env("SUSHI_PAIR"))

AMOUNT_IN_ETH = float(os.getenv("AMOUNT_IN_ETH", 0.5))
FEE_RATE = float(os.getenv("FEE_RATE", 0.003))
MIN_PROFIT_ETH = float(os.getenv("MIN_PROFIT_ETH", 0.005))

POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 2))
