import requests


class Handlers:
    def __init__(self, ulr_local_node):
        self.ulr_local_node = ulr_local_node
        self.base_data = {
            'id': 1,
            'jsonrpc': '2.0'
        }

    def get_account_balance(self, address: str):
        data = self.base_data
        data['method'] = 'eth_getBalance'
        data['params'] = [f'{address}', 'latest']
        response = requests.post(f'{self.ulr_local_node}', data=data)
        return response.json()['result']
