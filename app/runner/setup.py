from fastapi import FastAPI

from app.core.testservice import TestService
from app.infra.fastapi.test import api


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(api)
    app.state.core = TestService()
    return app
