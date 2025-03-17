import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TransferForm
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
BSC_RPC_URL = os.getenv("BSC_RPC_URL")
CONTRACT_ADDRESS = "0xf35270C748f97231F7B654F424704eABFF3DF53F"

# Connect to Binance Smart Chain
w3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
assert w3.is_connected(), "Failed to connect to BSC"

# Contract ABI (replace with your contract's ABI)
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

# Create contract instance
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# Get account
account = w3.eth.account.from_key(PRIVATE_KEY)

def index(request):
    balance = contract.functions.balanceOf(account.address).call()
    balance = w3.from_wei(balance, 'ether')
    return render(request, 'token_app/index.html', {'balance': balance})

def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            to_address = form.cleaned_data['to_address']
            amount = form.cleaned_data['amount']
            value = w3.to_wei(amount, 'ether')

            txn = contract.functions.transfer(to_address, value).build_transaction({
                "from": account.address,
                "nonce": w3.eth.get_transaction_count(account.address),
                "gas": 200000,
                "gasPrice": w3.to_wei("10", "gwei")
            })

            signed_txn = account.sign_transaction(txn)
            txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

            txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
            return HttpResponse(f"Tokens transferred. Transaction receipt: {txn_receipt}")

    else:
        form = TransferForm()
    return render(request, 'token_app/transfer.html', {'form': form})