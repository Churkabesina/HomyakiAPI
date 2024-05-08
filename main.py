from fastapi import FastAPI
from routes import private_routes, token_route
from db.core import __create_db

tags_metadata = [
    {
        'name': 'Auth',
        "description": "С ПОМОЩЬЮ ЭТОГО МЕТОДА МОЖНО ПОЛУЧИТЬ ТОКЕН"
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

app = FastAPI(title='Validium-test-net.API', openapi_tags=tags_metadata)

app.include_router(private_routes)

app.include_router(token_route)

__create_db()
