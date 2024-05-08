from fastapi import APIRouter, types, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
import handlers
import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/token')

token_route = APIRouter(prefix='/api', tags=['Auth'])

private_routes = APIRouter(prefix='/api', tags=['All endpoints'], dependencies=[Depends(oauth2_scheme)])


@token_route.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if form_data.username != 'admin' and form_data.password != 'admin123321':
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    return {"access_token": '0xf5300ba9fdf0412e1d2bc130e5932ee7da688c2773c1867ce83f38724b030c2f', "token_type": "bearer"}


@private_routes.get('/account.balance', tags=['1.Account'])
async def get_account_balance(account_address: str):
    result = handlers.get_account_balance(account_address)
    return result


@private_routes.post('/account.create', response_model=schemas.WalletPrivate, tags=['1.Account'])
async def create_account():
    result = handlers.create_account()
    return result


@private_routes.get('/account.nft_storage', response_model=schemas.NftStorage, tags=['1.Account'])
async def get_account_nft_storage(account_address: str):
    result = handlers.get_account_nft_storage(account_address)
    return result


@private_routes.post('/account.grant_ether', response_model=schemas.WalletTemp, tags=['1.Account'])
async def grant_ether(account_address: str, amount: int):
    result = handlers.grant_ether(account_address, amount)
    if result is None:
        raise HTTPException(status_code=403, detail='Account not found')
    return result


@private_routes.post('/contract.mint.result_storage_nft', tags=['Contract', '3.WinNFT'])
async def mint_result_storage_nft(account_address: str, data: schemas.ResultNftData):
    result = handlers.mint_result_storage_nft(account_address, data.data)
    return result


@private_routes.post('/contract.mint.ye_play_nft', response_model=schemas.MintYePlayResponse, tags=['Contract', '2.Buying a game'])
async def mint_ye_play_nft(account_address: str):
    result = handlers.mint_ye_play_nft(account_address)
    return result


@private_routes.post('/contract.buy_ye_play_nft', response_model=schemas.BuyYePlayResponse, tags=['Contract', '2.Buying a game'])
async def buy_ye_play_nft(account_address: str, value: int):
    result = handlers.buy_ye_play_nft(account_address, value)
    if result is None:
        raise HTTPException(status_code=403, detail='Account not found or insufficient funds')
    return result


@private_routes.delete('/contract.withdraw_nft_value', response_model=schemas.TxnStatus, tags=['Contract', '4.Vending machine'])
async def withdraw_nft_value(account_address: str, nft_id: int):
    result = handlers.withdraw_nft_value(account_address, nft_id)
    return result


@private_routes.get('/contract.results_balance', tags=['Contract'])
async def get_results_contract_balance():
    result = handlers.get_results_contract_balance()
    return result


@private_routes.get('/contract.ye_play_balance', tags=['Contract'])
async def get_ye_play_contract_balance():
    result = handlers.get_ye_play_contract_balance()
    return result


@private_routes.post('/contract.refill_balance', tags=['Contract'])
async def refill_contract_balance(value: int):
    result = handlers.refill_results_contract_balance(value)
    return result


# @private_routes.post('/contract.refill_ye_play_balance', tags=['Contract'])
# async def refill_ye_play_balance(value: int):
#     result = handlers.refill_ye_play_contract_balance(value)
#     return result


@private_routes.get('/contract.last_minted_nft', tags=['Contract'])
async def get_last_minted_nft_results():
    result = handlers.get_last_minted_nft_results()
    return result


@private_routes.get('/contract.nft_by_id', tags=['Contract'])
async def get_nft_by_id_results(nft_id: int):
    result = handlers.get_nft_by_id_results(nft_id)
    return result


@private_routes.post('/change_ye_play_status', response_model=schemas.MetaDataJson, tags=['2.Buying a game'])
async def change_ye_play_json_status(meta_data_uuid: str, new_status: bool):
    result = handlers.change_ye_play_json_status(meta_data_uuid, new_status)
    if result is None:
        raise HTTPException(status_code=403, detail='Meta data uuid file not found')
    return result


@private_routes.get('/txn_info', response_model=types.Dict, tags=['BezTega'])
async def get_txn_info(txn_hash: str):
    result = handlers.get_txn_info(txn_hash)
    return result


@private_routes.post('/get.test', tags=['BezTega'])
async def get_test():
    return 'TEST PROIDEN'
