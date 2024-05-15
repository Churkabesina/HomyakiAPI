import requests
import db
import ethereum_api
from eth_abi import decode as abi_decode
import json
import uuid
import os.path


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
    account_id = db.core.get_id_by_address(address)
    if account_id:
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
        res = {
            'id': account_id[0],
            'address': address
        }
        return res
    return None


def mint_ye_play_nft(address: str, data: str):
    meta_data_uuid = str(uuid.uuid4())
    meta_data_path = os.path.join('./json_storage', meta_data_uuid + '.json')
    encoded = ethereum.encode_function_call('mint_nft(address,string)', [address, meta_data_uuid])
    raw = ethereum.sign_smart_contract_txn(to=ethereum.ye_play_address, data=encoded, gas='0x200B20')
    txn_hash = ethereum.send_raw_txn(raw)
    res = {
        'meta_data_uuid': meta_data_uuid,
        'is_played': False,
        'data': data,
        'txn_hash': txn_hash,

    }
    json_obj = {
        'is_played': False,
        'data': data
    }
    with open(meta_data_path, 'w', encoding='UTF-8') as f:
        json.dump(json_obj, f, indent=4)
    return res


def buy_ye_play_nft(address: str, value: int, data: str):
    if get_account_balance(address) < value + 29184:
        return None
    private = db.core.get_private_by_address(address)
    if private:
        value = ethereum.w3.to_hex(value)
        private = private[0]
        encoded = ethereum.encode_function_call('refill_contract_balance()')
        raw = ethereum.sign_smart_contract_txn(to=ethereum.ye_play_address,
                                               data=encoded,
                                               gas='0x7200',
                                               value=value,
                                               account_from=(address, private))
        res_pay = ethereum.send_raw_txn(raw)
        res_mint = mint_ye_play_nft(address, data)
        res = {
            'meta_data_uuid': res_mint.get('meta_data_uuid'),
            'is_played': False,
            'data': data,
            'txn_hash': res_mint.get('txn_hash'),
            'pay_txn_hash': res_pay
        }
        return res
    return None


def change_ye_play_json_status(meta_data_uuid: str, new_status: bool):
    meta_data_path = os.path.join('./json_storage', meta_data_uuid + '.json')
    if not os.path.isfile(meta_data_path):
        return None
    with open(meta_data_path, 'r', encoding='UTF-8') as f:
        read_json = json.load(f)
        read_json['is_played'] = new_status
    with open(meta_data_path, 'w', encoding='UTF-8') as f:
        json.dump(read_json, f, indent=4)
    return {'meta_data_uuid': meta_data_uuid, 'is_played': new_status}


def check_ye_play_json_status(meta_data_uuid: str):
    meta_data_path = os.path.join('./json_storage', meta_data_uuid + '.json')
    if not os.path.isfile(meta_data_path):
        return None
    with open(meta_data_path, 'r', encoding='UTF-8') as f:
        read_json = json.load(f)
        read_json['meta_data_uuid'] = meta_data_uuid
    return read_json


def mint_result_storage_nft(address: str, data: int):
    encoded = ethereum.encode_function_call('mint_nft(address,uint256)', [address, data])
    raw = ethereum.sign_smart_contract_txn(to=ethereum.result_storage_address, data=encoded, gas='0x200B20')
    res = ethereum.send_raw_txn(raw)
    return res


def get_account_nft_storage(address: str):
    encoded = ethereum.encode_function_call('get_account_nft_storage(address)', [address])
    res = ethereum.call_smart_contract(to=ethereum.result_storage_address, data=encoded)
    res = {
        'account': address,
        'storage': abi_decode(['uint256[]'], res)[0]
    }
    return res


def withdraw_nft_value(address: str, nft_id: int):
    encoded = ethereum.encode_function_call('withdraw_nft_value(address,uint256)', [address, nft_id])
    raw = ethereum.sign_smart_contract_txn(to=ethereum.result_storage_address, data=encoded, gas='0x200B20')
    tx_hash = ethereum.send_raw_txn(raw)
    res = {'txn_hash': tx_hash, 'status': False}
    status = ethereum.w3.eth.wait_for_transaction_receipt(tx_hash)['status']
    if status == 1:
        res['status'] = True
    return res


def get_results_contract_balance():
    encoded = ethereum.encode_function_call('get_contract_balance()')
    res = ethereum.call_smart_contract(to=ethereum.result_storage_address, data=encoded)
    return ethereum.w3.to_int(res)


def get_ye_play_contract_balance():
    encoded = ethereum.encode_function_call('get_contract_balance()')
    res = ethereum.call_smart_contract(to=ethereum.ye_play_address, data=encoded)
    return ethereum.w3.to_int(res)


def refill_results_contract_balance(value: int):
    value = ethereum.w3.to_hex(value)
    encoded = ethereum.encode_function_call('refill_contract_balance()')
    raw = ethereum.sign_smart_contract_txn(to=ethereum.result_storage_address, data=encoded, value=value, gas='0x7200')
    res = ethereum.send_raw_txn(raw)
    return res


# def refill_ye_play_contract_balance(value: int):
#     value = ethereum.w3.to_hex(value)
#     encoded = ethereum.encode_function_call('refill_contract_balance()')
#     raw = ethereum.sign_smart_contract_txn(to=ethereum.ye_play_address, data=encoded, value=value, gas='0x7200')
#     res = ethereum.send_raw_txn(raw)
#     return res


def get_last_minted_nft_results():
    encoded = ethereum.encode_function_call('get_last_minted_nft()')
    res = ethereum.call_smart_contract(to=ethereum.result_storage_address, data=encoded)
    return ethereum.w3.to_int(res)


def get_nft_by_id_results(nft_id: int):
    encoded = ethereum.encode_function_call('get_nft_by_id(uint256)', [nft_id])
    res = ethereum.call_smart_contract(to=ethereum.result_storage_address, data=encoded)
    return ethereum.w3.to_int(res)


def get_txn_info(txn_hash: str):
    res = ethereum.w3.eth.get_transaction(txn_hash)
    return json.loads(ethereum.w3.to_json(res))
