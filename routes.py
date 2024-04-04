from typing import Annotated
from fastapi import APIRouter, HTTPException, Header
from handlers import Handlers

private_routes = APIRouter(prefix='/api')

handlers = Handlers('http://0.0.0.0:8123')


@private_routes.get('/account.balance')
async def get_account_balance(token: Annotated[str, Header()], account_address: str):
    if token != '12345':
        raise HTTPException(status_code=400, detail='Неверный токен')
    balance = handlers.get_account_balance(account_address)
    return balance
