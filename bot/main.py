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

def get_dynamic_gas_price():
    """Get current gas price with a small buffer."""
    try:
        base_fee = w3.eth.gas_price
        max_priority_fee = w3.toWei("2", "gwei")
        max_fee = int(base_fee * 1.1) + max_priority_fee
        return max_priority_fee, max_fee
    except Exception as e:
        print(f"Error getting gas price: {e}")
        return w3.toWei("2", "gwei"), w3.toWei("100", "gwei")

def check_arbitrage():
    rU0, rU1, _, _ = utils.get_reserves(pair_uni)
    rS0, rS1, _, _ = utils.get_reserves(pair_sushi)

    tokens_bought = utils.get_amount_out(AMOUNT_IN_WEI, rU0, rU1, config.FEE_RATE)
    eth_back = utils.get_amount_out(tokens_bought, rS1, rS0, config.FEE_RATE)
    profit_1 = eth_back - AMOUNT_IN_WEI
    
    tokens_bought_2 = utils.get_amount_out(AMOUNT_IN_WEI, rS0, rS1, config.FEE_RATE)
    eth_back_2 = utils.get_amount_out(tokens_bought_2, rU1, rU0, config.FEE_RATE)
    profit_2 = eth_back_2 - AMOUNT_IN_WEI
    
    min_profit_wei = w3.toWei(config.MIN_PROFIT_ETH, "ether")
    
    if profit_1 > min_profit_wei:
        print(f"✓ Uni->Sushi profit: {utils.wei_to_eth(w3, profit_1)} ETH")
        return True
    elif profit_2 > min_profit_wei:
        print(f"✓ Sushi->Uni profit: {utils.wei_to_eth(w3, profit_2)} ETH")
        return True
    else:
        print(f"✗ No profit")
        return False

def execute_trade():
    try:
        max_priority_fee, max_fee = get_dynamic_gas_price()
        nonce = w3.eth.get_transaction_count(ADDRESS)
        
        tx = arb_contract.functions.swap(AMOUNT_IN_WEI).buildTransaction({
            "from": ADDRESS,
            "nonce": nonce,
            "gas": 800000,
            "maxPriorityFeePerGas": max_priority_fee,
            "maxFeePerGas": max_fee,
            "chainId": config.CHAIN_ID
        })
        
        signed = acct.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        print(f"Trade submitted: {tx_hash.hex()}")
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        if receipt.status == 1:
            print(f"Success! Gas used: {receipt.gasUsed}")
        else:
            print(f"Transaction reverted")
            
    except Exception as e:
        print(f" Error: {e}")

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
