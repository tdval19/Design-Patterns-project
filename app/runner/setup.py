from pathlib import Path

from fastapi import FastAPI

from app.core.converter.bitcoin_converter import CexBitcoinConverter
from app.core.facade import BitcoinService
from app.core.interactors.statistics import StatisticInteractor
from app.core.interactors.transactions import TransactionsInteractor
from app.core.interactors.users import UserInteractor
from app.core.interactors.wallets import WalletInteractor
from app.infra.db.init_db import SqliteDbInitializer
from app.infra.db.rep.statistic_repository import SqlStatisticRepository
from app.infra.db.rep.transaction_repository import SqlTransactionRepository
from app.infra.db.rep.user_repository import SqlUserRepository
from app.infra.db.rep.wallet_repository import SqlWalletRepository
from app.infra.fastapi.api import api


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(api)

    db_path = Path(__file__).parent / "../infra/db/bitcoin_wallet.db"
    script_path = Path(__file__).parent / "../infra/db/scheme.sql"
    db = SqliteDbInitializer(script_path, str(db_path))
    wallet_rep = SqlWalletRepository(db.get_connection())
    statistics_rep = SqlStatisticRepository(db.get_connection())
    transaction_rep = SqlTransactionRepository(db.get_connection())
    user_rep = SqlUserRepository(db.get_connection())

    app.state.core = BitcoinService(
        StatisticInteractor(statistics_rep),
        WalletInteractor(wallet_rep),
        TransactionsInteractor(transaction_rep, wallet_rep),
        UserInteractor(user_rep),
        CexBitcoinConverter(),
    )
    return app
