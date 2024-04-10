import requests
import web3
import db


class Templates:
    ulr_local_node = 'http://0.0.0.0:8123'
    base_data = {
        'id': 1,
        'jsonrpc': '2.0'
    }
    headers = {
        'Content-Type': 'application/json'
    }


w3 = web3.Web3(web3.HTTPProvider(Templates.ulr_local_node))


def get_account_balance(address: str):
    data = Templates.base_data
    data['method'] = 'eth_getBalance'
    data['params'] = [f'{address}', 'latest']
    response = requests.post(f'{Templates.ulr_local_node}', json=data, headers=Templates.headers)
    result = int(response.json()['result'], 16)
    return result


def create_account():
    acc = w3.eth.account.create()
    key = w3.to_hex(acc.key)
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
    raw_hash = w3.eth.account.sign_transaction(
        transaction_dict={'from': '0x8F15C8eDb2974485957909E6fEEfc53972664cEC',
                          'to': address,
                          'value': w3.to_hex(amount),
                          'nonce': w3.eth.get_transaction_count(w3.to_checksum_address('0x8F15C8eDb2974485957909E6fEEfc53972664cEC'), 'latest'),
                          'gasPrice': '0x0',
                          'gas': '0x5208'},
        private_key='0x64205e253124acd904d403ef2627bda5a044efa63b5ced090f0f4e2f44bee6ec'
    )
    data['params'] = [raw_hash.rawTransaction]
    response = requests.post(f'{Templates.ulr_local_node}', json=data, headers=Templates.headers)
    result = response.json()
    print(result)
    return result


def grant_nft(address: str, data: str):
    return None


def buy_nft(account_address: str, data: str, value: int):
    return None