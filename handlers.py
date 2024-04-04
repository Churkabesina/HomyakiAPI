import requests


class Handlers:
    ulr_local_node = 'http://0.0.0.0:8123'
    base_data = {
        'id': 1,
        'jsonrpc': '2.0'
    }

    def get_account_balance(address: str):
        data = Handlers.base_data
        data['method'] = 'eth_getBalance'
        data['params'] = [f'{address}', 'latest']
        response = requests.post(f'{Handlers.ulr_local_node}', data=data)
        return response.json()['result']
