from fastapi import FastAPI
from routes import private_routes, token_route
from db.core import __create_db

app = FastAPI(title='Validium-test-net.API')

app.include_router(private_routes)

app.include_router(token_route)

__create_db()
