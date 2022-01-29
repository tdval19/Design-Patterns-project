from fastapi import APIRouter, Depends

from app.core.testservice import TestService
from app.infra.fastapi.dependables import get_core

api = APIRouter()


@api.get("/test")
def fetch_book(core: TestService = Depends(get_core)) -> str:
    return core.hello()
