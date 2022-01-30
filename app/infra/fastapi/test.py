from fastapi import APIRouter, Depends

from app.core.testservice import TestService
from app.infra.fastapi.dependables import get_core

api = APIRouter()


@api.get("/test")
def test(core: TestService = Depends(get_core)) -> str:
    return core.hello()


@api.get("/wallets")
def get_wallets(core: TestService = Depends(get_core)) -> str:
    pass


@api.get("/transactions")
def get_transactions(core: TestService = Depends(get_core)) -> str:
    pass


@api.get("/wallets/{address}/transactions")
def get_address_transactions(core: TestService = Depends(get_core)) -> str:
    pass


@api.get("/statistics")
def get_statistics(core: TestService = Depends(get_core)) -> str:
    pass


@api.post("/users")
def post_users(core: TestService = Depends(get_core)) -> str:
    pass


@api.post("/wallets")
def post_wallets(core: TestService = Depends(get_core)) -> str:
    pass


@api.post("/transactions")
def post_transactions(core: TestService = Depends(get_core)) -> str:
    pass


@api.post("/users")
def post_users(core: TestService = Depends(get_core)) -> str:
    pass
