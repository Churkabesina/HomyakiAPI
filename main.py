from fastapi import FastAPI
from routes import private_routes
from db.core import __create_db

app = FastAPI(title='Validium-test-net.API')

app.include_router(private_routes)

__create_db()
