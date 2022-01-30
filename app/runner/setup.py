from fastapi import FastAPI

from app.core.facade import BitcoinService
from app.infra.fastapi.test import api


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(api)
    app.state.core = BitcoinService()
    return app
