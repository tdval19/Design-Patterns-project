from fastapi import FastAPI

from app.core.converter.bitcoin_converter import CexBitcoinConverter
from app.core.facade import BitcoinService
from app.core.interactors.statistics import StatisticInteractor
from app.core.interactors.transactions import TransactionsInteractor
from app.core.interactors.users import UserInteractor
from app.core.interactors.wallets import WalletInteractor
from app.infra.db.rep.statistic_repository import SqlStatisticRepository
from app.infra.db.rep.transaction_repository import SqlTransactionRepository
from app.infra.db.rep.user_repository import SqlUserRepository
from app.infra.fastapi.test import api


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(api)
    db_name = "bitcoin_wallet.db"
    app.state.core = BitcoinService(
        StatisticInteractor(SqlStatisticRepository(db_name)),
        WalletInteractor(),
        TransactionsInteractor(SqlTransactionRepository(db_name)),
        UserInteractor(SqlUserRepository(db_name)),
        CexBitcoinConverter(),
    )
    return app
