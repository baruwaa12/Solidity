import json

from web3 import Web3

# In the video, we forget to `install_solc`
# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os


with open("SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

# # We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.6.0")

# Compile the solidity code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Gets bytecode - (object code that an interpreter converts into binary machine code)
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get the ABI (Application Binary Interface)
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

## To connect to ganache - use RPC Link on ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x150bc91e062314E211fe046b8b903159A8e6dCc4"
private_key = "0x699e2db8af7bfc3534522dffba61736eca53c6a515efa0d08397f456f5fb7f15"


# Create the contract in python.
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

# Build, sign and send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send this signed transaction to the blockchain
print("Deploying the contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Contract Deployed")


# Working with the contract - need 2 details Contract ABI and Contract Address
simple_Storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# 2 diff ways to interact with contract
# Call - Simulate making the call and getting a return value (No state change to the blockchain)
# Transact - Make a state change

# Initial value of favouriteNumber
print(simple_Storage.functions.retrieve().call())
print("Updating the contract...")
store_transaction = simple_Storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        # Nonce has to be different for every transaction
        "nonce": nonce + 1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
print("Updated!")
print(simple_Storage.functions.retrieve().call())
