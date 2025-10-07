import json
import os
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

load_dotenv()

RPC_HTTP = os.getenv("RPC_HTTP")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CHAIN_ID = int(os.getenv("CHAIN_ID", 1))

w3 = Web3(Web3.HTTPProvider(RPC_HTTP))
acct = w3.eth.account.from_key(PRIVATE_KEY)
ADDRESS = acct.address

install_solc("0.8.20") 
with open("contracts/ArbitrageExecutor.sol", "r") as f:
    source = f.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"ArbitrageExecutor.sol": {"content": source}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}},
    },
    solc_version="0.8.20",
)

abi = compiled_sol["contracts"]["ArbitrageExecutor.sol"]["ArbitrageExecutor"]["abi"]
bytecode = compiled_sol["contracts"]["ArbitrageExecutor.sol"]["ArbitrageExecutor"]["evm"]["bytecode"]["object"]


ArbContract = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(ADDRESS)

tx = ArbContract.constructor().buildTransaction({
    "from": ADDRESS,
    "nonce": nonce,
    "gas": 8000000,
    "gasPrice": w3.toWei("20", "gwei"),
    "chainId": CHAIN_ID,
})

signed_tx = acct.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print("Deployment transaction sent:", tx_hash.hex())

# Wait for receipt
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract deployed at:", receipt.contractAddress)
