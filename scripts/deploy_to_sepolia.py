import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Web3クラスのインスタンス作成
NODE_URL = os.getenv("ALCHEMY_URL")
w3 = Web3(Web3.HTTPProvider(NODE_URL))

# スマートコントラクトのインスタンス作成
contract_compiled_file = "../contracts/token.json"

with open(contract_compiled_file, "r", encoding="utf-16") as file:
    data = json.load(file)

bytecode = data["token.vy"]["bytecode"]
abi = data["token.vy"]["abi"]

contract = w3.eth.contract(bytecode=bytecode, abi=abi)

# トランザクションの構築
total_supply = 10000
account_1 = os.getenv("METAMASK_ACCOUNT_1")
nonce = w3.eth.get_transaction_count(account_1)
tx = contract.constructor(total_supply).build_transaction({'from': account_1, 'nonce': nonce})
 
# トランザクションの署名
private_key_1 = os.getenv("METAMASK_PRIVATE_KEY_1")
signed_tx = w3.eth.account.sign_transaction(tx, private_key_1)

# トランザクションの送信
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# トランザクションの完了待ち
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = {"contractAddress": tx_receipt["contractAddress"]}
contract_address_file = "../contracts/contractAddressSepolia.json"
with open(contract_address_file, "w") as file:
    json.dump(contract_address, file)