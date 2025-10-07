import time
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
from bot import utils, config

load_dotenv()

w3 = Web3(Web3.WebsocketProvider(config.RPC_WSS))
acct = Account.from_key(config.PRIVATE_KEY)
ADDRESS = acct.address

PAIR_ABI = [
    {"constant": True,"inputs": [],"name": "getReserves","outputs":[
        {"internalType": "uint112","name": "_reserve0","type": "uint112"},
        {"internalType": "uint112","name": "_reserve1","type": "uint112"},
        {"internalType": "uint32","name": "_blockTimestampLast","type": "uint32"}
    ],"stateMutability": "view","type": "function"},
    {"constant": True,"inputs": [],"name": "token0","outputs":[{"name": "", "type": "address"}],"stateMutability":"view","type":"function"},
    {"constant": True,"inputs": [],"name": "token1","outputs":[{"name": "", "type": "address"}],"stateMutability":"view","type":"function"}
]

ARBITRAGE_ABI = [
    {"inputs":[{"internalType":"uint256","name":"_amountIn","type":"uint256"}],
     "name":"swap","outputs":[],"stateMutability":"nonpayable","type":"function"}
]


pair_uni = w3.eth.contract(address=config.UNIV2_PAIR, abi=PAIR_ABI)
pair_sushi = w3.eth.contract(address=config.SUSHI_PAIR, abi=PAIR_ABI)
arb_contract = w3.eth.contract(address=config.ARBITRAGE_CONTRACT, abi=ARBITRAGE_ABI)

AMOUNT_IN_WEI = w3.toWei(config.AMOUNT_IN_ETH, "ether")

def check_arbitrage():
    rU0, rU1, _, _ = utils.get_reserves(pair_uni)
    rS0, rS1, _, _ = utils.get_reserves(pair_sushi)

    tokens_bought = utils.get_amount_out(AMOUNT_IN_WEI, rU0, rU1, config.FEE_RATE)
    eth_back = utils.get_amount_out(tokens_bought, rS1, rS0, config.FEE_RATE)

    profit = eth_back - AMOUNT_IN_WEI
    print(f"Profit estimate: {utils.wei_to_eth(w3, profit)} ETH")
    return profit > w3.toWei(config.MIN_PROFIT_ETH, "ether")

def execute_trade():
    nonce = w3.eth.get_transaction_count(ADDRESS)
    tx = arb_contract.functions.swap(AMOUNT_IN_WEI).buildTransaction({
        "from": ADDRESS,
        "nonce": nonce,
        "gas": 800000,
        "maxPriorityFeePerGas": w3.toWei("2", "gwei"),
        "maxFeePerGas": w3.toWei("120", "gwei"),
        "chainId": config.CHAIN_ID
    })
    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    print("Trade submitted:", tx_hash.hex())

def main():
    while True:
        try:
            if check_arbitrage():
                print("Profitable arbitrage detected! Executing...")
                execute_trade()
            else:
                print("No profitable opportunity.")
        except Exception as e:
            print("Error:", e)
        time.sleep(config.POLL_INTERVAL)

if __name__ == "__main__":
    main()
