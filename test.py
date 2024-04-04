import requests

address = '0x3A63c4477f84Cc60A32ad28C8098cA12B1eC2bfa'
res = requests.get(f'http://localhost:8123/api/account.balance?account_address={address}', headers={'token': '1234'})
print(res.status_code)
print(res.json())
