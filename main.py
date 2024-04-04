from fastapi import FastAPI
from routes import private_routes

app = FastAPI(title='Homyaki-test-net.API')

app.include_router(private_routes)
