import json
from web3 import Web3

# Web3クラスのインスタンス作成
NODE_URL = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(NODE_URL))

# スマートコントラクトのインスタンス作成
contract_compiled_file = "../contracts/token.json"

with open(contract_compiled_file, "r", encoding="utf-16") as file:
    data = json.load(file)

abi = data["token.vy"]["abi"]

contract_address_file = "../contracts/contractAddressGanache.json"

with open(contract_address_file, "r", encoding="utf-8") as file:
    data = json.load(file)

contract_address = data["contractAddress"]

contract = w3.eth.contract(address=contract_address, abi=abi)

# totalSupply
totalSupply = contract.functions.totalSupply().call()
print(f"totalSupply: {totalSupply}")

# balances
account_1 = "Ganacheのアカウント1"
account_2 = "Ganacheのアカウント2"

balance_1 = contract.functions.balances(account_1).call()
balance_2 = contract.functions.balances(account_2).call()

print(f"balance_1: {balance_1}")
print(f"balance_2: {balance_2}")

# external_func
external_func = contract.functions.external_func("abc").call()
print(f"external_func: {external_func}")

# dummy
# dummy = contract.functions.dummy().call()
# print(f"dummy: {dummy}")

# internal_func
# internal_func = contract.functions.internal_func(333).call()
# print(f"internal_func: {internal_func}")

# トランザクションの構築
nonce = w3.eth.get_transaction_count(account_1)
tx = contract.functions.transfer(account_2, 100).build_transaction({'from': account_1, 'nonce': nonce})

# トランザクションの署名
private_key_1 = "Ganacheのプライベートキー1(頭の0xは除く)"
signed_tx = w3.eth.account.sign_transaction(tx, private_key_1)

# トランザクションの送信
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# トランザクションの完了待ち
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# transfer後
balance_1 = contract.functions.balances(account_1).call()
balance_2 = contract.functions.balances(account_2).call()

print(f"transfer後 balance_1: {balance_1}")
print(f"transfer後 balance_2: {balance_2}")

# イベント
transfer_log = contract.events.Transfer().process_receipt(tx_receipt)

print(f"sender: {transfer_log[0]['args']['sender']}")
print(f"receiver: {transfer_log[0]['args']['receiver']}")
print(f"value: {transfer_log[0]['args']['value']}")