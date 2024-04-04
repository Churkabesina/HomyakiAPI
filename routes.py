from typing import Annotated
from fastapi import APIRouter, HTTPException, Header
import handlers

private_routes = APIRouter(prefix='/api')


@private_routes.get('/account.balance')
async def get_account_balance(token: Annotated[str, Header()], account_address: str):
    if token != '12345':
        raise HTTPException(status_code=400, detail='Неверный токен')
    balance = handlers.get_account_balance(account_address)
    return balance
