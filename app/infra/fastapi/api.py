from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.facade import BitcoinService
from app.core.interactors.transactions import NotEnoughBitcoinsException
from app.core.interactors.users import UserNotFoundException
from app.core.interactors.wallets import (
    WalletNotFoundException,
    UserReachedWalletLimitException,
)
from app.core.models.transaction import Transaction
from app.infra.fastapi.dependables import get_core

api = APIRouter()


class WalletRequest(BaseModel):
    user_id: int


class WalletResponse(BaseModel):
    address: int
    balance_btc: float
    balance_usd: float


class TransactionRequest(BaseModel):
    wallet_address_from: int
    wallet_address_to: int
    amount_btc: float


class TransactionResponse(BaseModel):
    wallet_address_from: int
    wallet_address_to: int
    amount_btc: float


class TransactionsResponse(BaseModel):
    transactions_list: List[TransactionResponse]


class StatisticsResponse(BaseModel):
    num_of_transactions: int
    total_profit: float


def parse_transaction_list(lst: List[Transaction]) -> TransactionsResponse:
    result_list = []
    for transaction in lst:
        result_list.append(
            TransactionResponse(
                wallet_address_from=transaction.from_address,
                wallet_address_to=transaction.to_address,
                amount_btc=transaction.amount,
            )
        )
    return TransactionsResponse(transactions_list=result_list)


@api.get("/wallets/{address}", tags=["wallets"])
def get_wallets(
    address: int,
    core: BitcoinService = Depends(get_core),
) -> WalletResponse:
    wallet = None
    try:
        wallet = core.get_wallet(address)
    except WalletNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)

    return WalletResponse(
        address=wallet.wallet_address,
        balance_btc=wallet.balance_btc,
        balance_usd=core.convert_bitcoin_to("USD", wallet.balance_btc),
    )


@api.get("/transactions", tags=["transactions"])
def get_user_transactions(
    user_id: int, core: BitcoinService = Depends(get_core)
) -> TransactionsResponse:
    transaction_list = None

    try:
        transaction_list = core.get_user_transactions(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)

    return parse_transaction_list(transaction_list)


@api.get("/wallets/{address}/transactions", tags=["transactions"])
def get_wallet_transactions(
    address: int, core: BitcoinService = Depends(get_core)
) -> TransactionsResponse:
    transaction_list = None

    try:
        transaction_list = core.get_wallet_transactions(address)
    except WalletNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)

    return parse_transaction_list(transaction_list)


@api.get("/statistics", tags=["statistics"])
def get_statistics(
    admin_key: str,
    core: BitcoinService = Depends(get_core),
) -> StatisticsResponse:
    stats = core.get_statistics(admin_key)
    return StatisticsResponse(
        num_of_transactions=stats.num_of_transactions, total_profit=stats.total_profit
    )


@api.post("/users", tags=["users"])
def create_user(core: BitcoinService = Depends(get_core)) -> int:
    return core.create_user().user_id


@api.post("/wallets", tags=["wallets"])
def create_wallet(
    request: WalletRequest,
    core: BitcoinService = Depends(get_core),
) -> WalletResponse:
    wallet = None
    try:
        wallet = core.create_wallet(request.user_id)
    except UserReachedWalletLimitException as e:
        raise HTTPException(status_code=400, detail=e.message)

    return WalletResponse(
        address=wallet.wallet_address,
        balance_btc=wallet.balance_btc,
        balance_usd=core.convert_bitcoin_to("USD", wallet.balance_btc),
    )


@api.post("/transactions", tags=["transactions"])
def make_transaction(
    request: TransactionRequest, core: BitcoinService = Depends(get_core)
) -> None:
    try:
        core.make_transaction(
            Transaction(
                request.wallet_address_from,
                request.wallet_address_to,
                request.amount_btc,
            )
        )
    except WalletNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except NotEnoughBitcoinsException as e1:
        raise HTTPException(status_code=400, detail=e1.message)
