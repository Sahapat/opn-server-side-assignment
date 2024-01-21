from fastapi import FastAPI
from .dependency import inject
async def on_startup(app: FastAPI):
    inject()

async def on_shutdown(app: FastAPI):
    pass
