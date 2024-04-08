from typing import Annotated
from fastapi import APIRouter, HTTPException, Header
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


@private_routes.post('/grant.ether', response_model=schemas.Wallet)
async def grant_ether(account_address: str, amount: int):
    result = handlers.grant_ether(account_address, amount)
    return result


@private_routes.post('/grant.nft')
async def grant_nft(account_address: str, data: str):
    result = handlers.grant_nft(account_address, data)
    return result
