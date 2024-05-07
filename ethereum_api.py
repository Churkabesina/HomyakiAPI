from hexbytes import HexBytes
import web3
from eth_abi import encode
from eth_abi.packed import encode_packed
import codecs


class EthereumAPI:
    def __init__(self, provider: str, main_account: tuple):
        self.w3 = web3.Web3(web3.HTTPProvider(provider))
        self.main_account = main_account
        self.result_storage_address = '0x1d7B96802FdB4C3d409c6931Ea8e7A79418C787F'
        self.ye_play_address = '0x660A7f98214b02cDBe65559aD4EcB4dA08993c79'

    def sign_txn(self, to, value, gas, gas_price, account: tuple = None):
        if account:
            from_address, private_key = account
        else:
            from_address, private_key = self.main_account

    def sign_smart_contract_deploy(self, data: str,
                                   account_from: tuple[str, str] = None,
                                   value: str = '0x0',
                                   gas: str = '0x1C9C380',
                                   gas_price: str = '0x0',):
        if account_from:
            from_address, private_key = account_from
        else:
            from_address, private_key = self.main_account
        tx_dict = {
            'from': from_address,
            'value': value,
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': self.w3.eth.get_transaction_count(from_address, 'latest'),
            'data': data
        }
        return self.w3.eth.account.sign_transaction(tx_dict, private_key=private_key).rawTransaction

    def deploy_smart_contract(self, data: str,
                              account_from: tuple[str, str] = None,
                              value: str = '0x0',
                              gas: str = '0x1C9C380',
                              gas_price: str = '0x0'):
        if account_from:
            from_address, private_key = account_from
        else:
            from_address, private_key = self.main_account
        raw = self.sign_smart_contract_deploy(data=data, account_from=(from_address, private_key), value=value, gas=gas, gas_price=gas_price)
        res = self.send_raw_txn(raw)
        return res

    def sign_smart_contract_txn(self, data: str,
                                to: str,
                                account_from: tuple[str, str] = None,
                                value: str = '0x0',
                                gas: str = '0x5208',
                                gas_price: str = '0x0'):
        if account_from:
            from_address, private_key = account_from
        else:
            from_address, private_key = self.main_account
        tx_dict = {
            'from': from_address,
            'to': to,
            'value': value,
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': self.w3.eth.get_transaction_count(from_address, 'latest'),
            'data': data
        }
        return self.w3.eth.account.sign_transaction(tx_dict, private_key=private_key).rawTransaction

    def send_raw_txn(self, raw_txn: HexBytes):
        return self.w3.eth.send_raw_transaction(raw_txn).hex()

    def call_smart_contract(self, to: str, data: str):
        res = self.w3.eth.call({'to': to, 'data': data}, 'latest')
        return res

    def encode_function_call(self, function_name: str, values: list | None = None, packed: bool = False) -> str:
        func_keccak = self.w3.keccak(text=function_name).hex()[:10]
        types = self._find_types(function_name)
        if packed:
            encoded_params = encode_packed(types, values).hex() if values else ''
        else:
            encoded_params = encode(types, values).hex() if values else ''
        encoded_func_call = func_keccak + encoded_params
        return encoded_func_call

    @staticmethod
    def _find_types(func_name: str):
        slice_start = func_name.find('(') + 1
        return func_name[slice_start:-1].split(',')

    @staticmethod
    def encode_string_to_int(data: str) -> str:
        encoded = int.from_bytes(bytes(data, 'utf-8'), byteorder='little')
        return str(encoded)

    @staticmethod
    def decode_int_to_string(data: int) -> str:
        decoded = data.to_bytes((data.bit_length() + 7) // 8, byteorder='little')
        return decoded.decode('utf-8')

    @staticmethod
    def convert_to_bytes_massive(data: str) -> list[bytes]:
        fraction = 20
        count_fractions = len(data) // fraction
        massive = []
        for x in range(count_fractions):
            text_slice = data[x * fraction:(x + 1) * fraction]
            massive.append(bytes(text_slice, 'utf-8'))
            if x == count_fractions - 1:
                text_slice = data[(x + 1) * fraction:]
                massive.append(bytes(text_slice, 'utf-8'))
        return massive

    @staticmethod
    def bytes32_decode_to_int(data: HexBytes) -> int:
        clear_massive = data[64:]
        output_str = ''
        for bytes32_elem_index in range(len(clear_massive) // 32):
            bytes32_elem = clear_massive[bytes32_elem_index * 32:(bytes32_elem_index + 1) * 32]
            clear_elem = bytes32_elem.hex().rstrip('0')
            if len(clear_elem) % 2 != 0:
                clear_elem += '0'
            decoded_elem = codecs.decode(clear_elem, 'hex')
            output_str += decoded_elem.decode('utf-8')
        return int(output_str)
