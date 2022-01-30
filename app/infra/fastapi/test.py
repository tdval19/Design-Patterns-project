from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.facade import BitcoinService
from app.infra.fastapi.dependables import get_core

api = APIRouter()


class WalletResponse(BaseModel):
    address: int
    balance_btc: float
    balance_usd: float


class TransactionRequest(BaseModel):
    address_from: int
    address_to: int
    amount_btc: float


class TransactionResponse(BaseModel):
    address_from: int
    address_to: int
    amount_btc: float
    amount_usd: float


class TransactionsResponse(BaseModel):
    transactions_list: List[TransactionResponse]


class StatisticsResponse(BaseModel):
    num_of_transactions: int
    total_profit: float


@api.get("/wallets/{address}")
def get_wallets(
    user_id: int, address: int, core: BitcoinService = Depends(get_core)
) -> WalletResponse:
    pass


@api.get("/transactions")
def get_transactions(
    user_id: int, core: BitcoinService = Depends(get_core)
) -> TransactionsResponse:
    pass


@api.get("/wallets/{address}/transactions")
def get_address_transactions(
    user_id: int, address: int, core: BitcoinService = Depends(get_core)
) -> TransactionsResponse:
    pass


@api.get("/statistics")
def get_statistics(
    admin_key: int, core: BitcoinService = Depends(get_core)
) -> StatisticsResponse:
    pass


@api.post("/users")
def post_users(core: BitcoinService = Depends(get_core)) -> int:
    pass


@api.post("/wallets")
def post_wallets(
    api_key: int, core: BitcoinService = Depends(get_core)
) -> WalletResponse:
    pass


@api.post("/transactions")
def post_transactions(
    api_key: int, request: TransactionRequest, core: BitcoinService = Depends(get_core)
) -> None:
    pass
