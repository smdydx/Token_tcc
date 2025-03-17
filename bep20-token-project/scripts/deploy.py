import json
import os
from web3 import Web3
from solcx import compile_source, install_solc
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
BSC_RPC_URL = os.getenv("BSC_RPC_URL")

# ✅ Install Solidity compiler if not installed
install_solc("0.8.26")

# ✅ Connect to Binance Smart Chain Testnet
w3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
assert w3.is_connected(), "Failed to connect to BSC"

# ✅ Get Absolute Path for Solidity Contract
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # scripts folder ka path
CONTRACT_PATH = os.path.join(CURRENT_DIR, "..", "contracts", "MyToken.sol")

# ✅ Compile Solidity contract
def compile_contract():
    if not os.path.exists(CONTRACT_PATH):
        raise FileNotFoundError(f"❌ Contract file not found: {CONTRACT_PATH}")

    with open(CONTRACT_PATH, "r") as file:
        solidity_code = file.read()

    compiled_sol = compile_source(solidity_code, solc_version="0.8.26")
    contract_id, contract_interface = compiled_sol.popitem()
    return contract_interface

# ✅ Deploy contract
def deploy_contract():
    contract_interface = compile_contract()

    # Get account
    account = w3.eth.account.from_key(PRIVATE_KEY)

    # Create contract instance
    Contract = w3.eth.contract(abi=contract_interface["abi"], bytecode=contract_interface["bin"])

    # Build and sign transaction
    txn = Contract.constructor().build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 2000000,
        "gasPrice": w3.to_wei("10", "gwei")
    })

    signed_txn = account.sign_transaction(txn)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f"⏳ Deploying contract... Transaction Hash: {txn_hash.hex()}")

    # Wait for transaction confirmation
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    print(f"✅ Contract deployed at address: {txn_receipt.contractAddress}")

if __name__ == "__main__":
    deploy_contract()