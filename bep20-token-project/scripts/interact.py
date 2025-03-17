import os
from web3 import Web3
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
BSC_RPC_URL = os.getenv("BSC_RPC_URL")
CONTRACT_ADDRESS = "0xf35270C748f97231F7B654F424704eABFF3DF53F"

# ✅ Connect to Binance Smart Chain
w3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
assert w3.is_connected(), "Failed to connect to BSC"

# ✅ Contract ABI (replace with your contract's ABI)
contract_abi = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# ✅ Create contract instance
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# ✅ Get account
account = w3.eth.account.from_key(PRIVATE_KEY)

# ✅ Transfer tokens
def transfer_tokens(to_address, amount):
    # Convert amount to Wei according to decimals (18)
    value = w3.to_wei(amount, 'ether')

    # Build and sign transaction
    txn = contract.functions.transfer(to_address, value).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 200000,
        "gasPrice": w3.to_wei("10", "gwei")
    })

    signed_txn = account.sign_transaction(txn)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f"⏳ Transferring tokens... Transaction Hash: {txn_hash.hex()}")

    # Wait for transaction confirmation
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    print(f"✅ Tokens transferred. Transaction receipt: {txn_receipt}")

# ✅ Check balance
def check_balance(address):
    balance = contract.functions.balanceOf(address).call()
    print(f"Balance of {address}: {w3.from_wei(balance, 'ether')} MTK")

if __name__ == "__main__":
    # Example: Transfer 10 tokens to another address
    transfer_tokens("0xF1F09492f4bDE390B5892268f3cd2741a5042908", 10)

    # Example: Check balance of your account
    check_balance(account.address)