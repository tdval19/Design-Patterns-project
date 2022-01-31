from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.converter.bitcoin_converter import IBitcoinConverter
from app.core.facade import BitcoinService
from app.infra.fastapi.dependables import get_core, get_converter

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


@api.get("/wallets/{address}", tags=["wallets"])
def get_wallets(
    user_id: int,
    address: int,
    core: BitcoinService = Depends(get_core),
    converter: IBitcoinConverter = Depends(get_converter),
) -> WalletResponse:
    pass


@api.get("/transactions", tags=["transactions"])
def get_transactions(
    user_id: int, core: BitcoinService = Depends(get_core)
) -> TransactionsResponse:
    pass


@api.get("/wallets/{address}/transactions", tags=["transactions"])
def get_wallet_transactions(
    user_id: int, address: int, core: BitcoinService = Depends(get_core)
) -> TransactionsResponse:
    pass


@api.get("/statistics", tags=["statistics"])
def get_statistics(
    admin_key: int,
    core: BitcoinService = Depends(get_core),
    converter: IBitcoinConverter = Depends(get_converter),
) -> StatisticsResponse:
    pass


@api.post("/users", tags=["users"])
def create_user(core: BitcoinService = Depends(get_core)) -> int:
    pass


@api.post("/wallets", tags=["wallets"])
def create_wallet(
    api_key: int,
    core: BitcoinService = Depends(get_core),
    converter: IBitcoinConverter = Depends(get_converter),
) -> WalletResponse:
    pass


@api.post("/transactions", tags=["transactions"])
def make_transaction(
    api_key: int, request: TransactionRequest, core: BitcoinService = Depends(get_core)
) -> None:
    pass
