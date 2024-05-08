from fastapi import FastAPI
from routes import private_routes, token_route
from db.core import __create_db

tags_metadata = [
    {
        'name': 'Auth',
    },
    {
        'name': '1.Account'
    },
    {
        'name': '2.Buying a game'
    },
    {
        'name': '3.WinNFT'
    },
    {
        'name': '4.Vending machine'
    },
    {
        'name': 'AllEndpoints'
    }
]

app = FastAPI(title='Validium-test-net.API')

app.include_router(private_routes)

app.include_router(token_route)

__create_db()
