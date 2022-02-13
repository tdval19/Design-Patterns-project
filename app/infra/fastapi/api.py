from typing import List, Optional

from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, PositiveFloat

from app.core.facade import BitcoinService
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
    amount_btc: PositiveFloat


class TransactionResponse(BaseModel):
    wallet_address_from: int
    wallet_address_to: int
    amount_btc: float


class TransactionsResponse(BaseModel):
    transactions_list: List[TransactionResponse]


class StatisticsResponse(BaseModel):
    num_of_transactions: int
    total_profit: float


class UserResponse(BaseModel):
    key: str


class TransactionSuccessResponse(BaseModel):
    message: str = "transaction was made successfully"


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


@api.get("/wallets/{address}", tags=["wallets"], response_model=WalletResponse)
def get_wallet(
    address: int,
    key: Optional[str] = Header(None),
    core: BitcoinService = Depends(get_core),
) -> WalletResponse:
    wallet = core.get_wallet(key, address)

    return WalletResponse(
        address=wallet.wallet_address,
        balance_btc=wallet.balance_btc,
        balance_usd=core.convert_bitcoin_to("USD", wallet.balance_btc),
    )


@api.get("/transactions", tags=["transactions"], response_model=TransactionsResponse)
def get_user_transactions(
    key: Optional[str] = Header(None), core: BitcoinService = Depends(get_core)
) -> TransactionsResponse:
    transaction_list = core.get_user_transactions(key)

    return parse_transaction_list(transaction_list)


@api.get(
    "/wallets/{address}/transactions",
    tags=["transactions"],
    response_model=TransactionsResponse,
)
def get_wallet_transactions(
    address: int,
    key: Optional[str] = Header(None),
    core: BitcoinService = Depends(get_core),
) -> TransactionsResponse:
    transaction_list = core.get_wallet_transactions(key, address)

    return parse_transaction_list(transaction_list)


@api.get("/statistics", tags=["statistics"], response_model=StatisticsResponse)
def get_statistics(
    admin_key: Optional[str] = Header(None),
    core: BitcoinService = Depends(get_core),
) -> StatisticsResponse:
    stats = core.get_statistics(admin_key)

    return StatisticsResponse(
        num_of_transactions=stats.num_of_transactions, total_profit=stats.total_profit
    )


@api.post("/users", tags=["users"], response_model=UserResponse)
def create_user(core: BitcoinService = Depends(get_core)) -> UserResponse:
    return UserResponse(key=core.create_user())


@api.post("/wallets", tags=["wallets"], response_model=WalletResponse)
def create_wallet(
    key: Optional[str] = Header(None),
    core: BitcoinService = Depends(get_core),
) -> WalletResponse:
    wallet = core.create_wallet(key)

    return WalletResponse(
        address=wallet.wallet_address,
        balance_btc=wallet.balance_btc,
        balance_usd=core.convert_bitcoin_to("USD", wallet.balance_btc),
    )


@api.post(
    "/transactions", tags=["transactions"], response_model=TransactionSuccessResponse
)
def make_transaction(
    request: TransactionRequest,
    key: Optional[str] = Header(None),
    core: BitcoinService = Depends(get_core),
) -> TransactionSuccessResponse:
    core.make_transaction(
        key,
        Transaction(
            request.wallet_address_from,
            request.wallet_address_to,
            request.amount_btc,
        ),
    )
    return TransactionSuccessResponse(message="Transaction was made successfully")
