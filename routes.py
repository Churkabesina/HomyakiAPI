from fastapi import APIRouter
import handlers
import schemas

private_routes = APIRouter(prefix='/api', tags=['All endpoints'])


@private_routes.get('/account.balance')
async def get_account_balance(account_address: str):
    result = handlers.get_account_balance(account_address)
    return result


@private_routes.put('/account.create', response_model=schemas.WalletPrivate)
async def create_account():
    result = handlers.create_account()
    return result


@private_routes.post('/account.nft_storage')
async def get_account_nft_storage(account_address: str):
    result = handlers.get_account_nft_storage(account_address)
    return result


@private_routes.post('/account.grant_ether', response_model=schemas.Wallet)
async def grant_ether(account_address: str, amount: int):
    result = handlers.grant_ether(account_address, amount)
    return result


@private_routes.post('/mint.result_storage_nft')
async def mint_result_storage_nft(account_address: str, data: schemas.ResultNftData):
    result = handlers.mint_result_storage_nft(account_address, data.data)
    return result


@private_routes.post('/mint.ye_play_nft')
async def mint_ye_play_nft(account_address: str, data: schemas.YEplayNftData):
    result = handlers.mint_ye_play_nft(account_address, data.data)
    return result


@private_routes.post('/contract.withdraw_nft_value')
async def withdraw_nft_value(account_address: str, nft_id: int):
    result = handlers.withdraw_nft_value(account_address, nft_id)
    return result


@private_routes.get('/contract.balance')
async def get_results_contract_balance():
    result = handlers.get_results_contract_balance()
    return result


@private_routes.post('/contract.refill_balance')
async def refill_contract_balance(value: int):
    result = handlers.refill_contract_balance(value)
    return result
