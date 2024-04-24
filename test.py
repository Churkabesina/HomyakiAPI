import requests

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

data = {
    'data': '123'
}

res = requests.post(f'http://185.137.233.141:25363/api/mint.ye_play_nft?account_address=0x47D383466926400342991b67804Cf6d0e57cc201', json=data, headers=headers)
print(res.status_code)
print(res.json())
