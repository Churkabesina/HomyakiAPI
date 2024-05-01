import requests
import web3
import db
import ethereum_api


class Templates:
    ulr_local_node = 'http://0.0.0.0:8123'
    base_data = {
        'id': 1,
        'jsonrpc': '2.0'
    }
    headers = {
        'Content-Type': 'application/json'
    }


acc = ('0x8F15C8eDb2974485957909E6fEEfc53972664cEC', '0x64205e253124acd904d403ef2627bda5a044efa63b5ced090f0f4e2f44bee6ec')
ethereum = ethereum_api.EthereumAPI('http://127.0.0.1:8123', acc)


def get_account_balance(address: str):
    data = Templates.base_data
    data['method'] = 'eth_getBalance'
    data['params'] = [f'{address}', 'latest']
    response = requests.post(f'{Templates.ulr_local_node}', json=data, headers=Templates.headers)
    result = int(response.json()['result'], 16)
    return result


def create_account():
    acc = ethereum.w3.eth.account.create()
    key = ethereum.w3.to_hex(acc.key)
    address = acc.address
    result = db.core.insert_wallet(address, key)
    result = {
        'id': result,
        'address': address,
        'balance': 0,
        'key': key
    }
    return result


def grant_ether(address: str, amount: int):
    data = Templates.base_data
    data['method'] = 'eth_sendRawTransaction'
    raw_hash = ethereum.w3.eth.account.sign_transaction(
        transaction_dict={'from': '0x8F15C8eDb2974485957909E6fEEfc53972664cEC',
                          'to': address,
                          'value': ethereum.w3.to_hex(amount),
                          'nonce': ethereum.w3.eth.get_transaction_count(ethereum.w3.to_checksum_address('0x8F15C8eDb2974485957909E6fEEfc53972664cEC'), 'latest'),
                          'gasPrice': '0x0',
                          'gas': '0x5208'},
        private_key='0x64205e253124acd904d403ef2627bda5a044efa63b5ced090f0f4e2f44bee6ec'
    )
    data['params'] = [raw_hash.rawTransaction.hex()]
    requests.post(f'{Templates.ulr_local_node}', json=data, headers=Templates.headers)
    old_balance = get_account_balance(address)
    new_balance = old_balance + amount
    db.core.update_account_balance(address, new_balance)
    account_id = db.core.get_id_by_address(address)
    res = {
        'id': account_id,
        'address': address,
        'balance': new_balance
    }
    return res


def mint_ye_play_nft(address: str, data: str):
    encoded = ethereum.encode_function_call('mint_nft(address,string)', [address, data])
    raw = ethereum.sign_smart_contract_txn(to=ethereum.ye_play_address, data=encoded, gas='0x200B20')
    res = ethereum.send_raw_txn(raw)
    return res


def mint_result_storage_nft(address: str, data: int):
    encoded = ethereum.encode_function_call('mint_nft(address,uint256)', [address, data])
    raw = ethereum.sign_smart_contract_txn(to=ethereum.result_storage_address, data=encoded, gas='0x200B20')
    res = ethereum.send_raw_txn(raw)
    return res


def get_account_nft_storage(address: str):
    encoded = ethereum.encode_function_call('get_account_nft_storage()', [address])
    res = ethereum.call_smart_contract(to=ethereum.result_storage_address, data=encoded)
    return res


def withdraw_nft_value(address: str, nft_id: int):
    encoded = ethereum.encode_function_call('withdraw_nft_value(address,uint256)', [address, nft_id])
    raw = ethereum.sign_smart_contract_txn(to=ethereum.result_storage_address, data=encoded, gas='0x200B20')
    res = ethereum.send_raw_txn(raw)
    return res


def get_results_contract_balance():
    encoded = ethereum.encode_function_call('get_contract_balance()')
    res = ethereum.call_smart_contract(to=ethereum.result_storage_address, data=encoded)
    return res


def refill_contract_balance(value: int):
    value = ethereum.w3.toHex(value)
    encoded = ethereum.encode_function_call('refill_contract_balance()')
    raw = ethereum.sign_smart_contract_txn(to=ethereum.result_storage_address, data=encoded, value=value)
    res = ethereum.send_raw_txn(raw)
    return res
