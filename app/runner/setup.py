from pathlib import Path

from fastapi import FastAPI

from app.core.converter.bitcoin_converter import CexBitcoinConverter
from app.core.facade import BitcoinService
from app.core.interactors.auth import (
    SimpleAuth,
    NotAuthorizedException,
    ForbiddenException,
)
from app.core.interactors.statistics import StatisticInteractor
from app.core.interactors.transactions import (
    TransactionsInteractor,
    NotEnoughBitcoinsException,
)
from app.core.interactors.users import UserInteractor, UserNotFoundException
from app.core.interactors.wallets import (
    WalletInteractor,
    WalletNotFoundException,
    UserReachedWalletLimitException,
)
from app.infra.db.init_db import SqliteDbInitializer
from app.infra.db.rep.statistic_repository import SqlStatisticRepository
from app.infra.db.rep.transaction_repository import SqlTransactionRepository
from app.infra.db.rep.user_repository import SqlUserRepository
from app.infra.db.rep.wallet_repository import SqlWalletRepository
from app.infra.encoder.dummy_encoder import SimpleKeyEncoder
from app.infra.fastapi.api import api
from app.infra.fastapi.api_exception_handlers import (
    user_not_found_exception_handler,
    wallet_not_found_exception_handler,
    not_authorized_exception_handler,
    forbidden_access_exception_handler,
    not_enough_bitcoins_exception_handler,
    user_reached_wallet_limit_exception_handler,
)

real_db_path = Path(__file__).parent / "../infra/db/bitcoin_wallet.db"
script_path = Path(__file__).parent / "../infra/db/scheme.sql"


def get_api() -> FastAPI:
    return setup(db_path=str(real_db_path), script=script_path)


def setup_test_api() -> FastAPI:
    return setup(db_path=":memory:", script=script_path)


def setup(db_path: str, script: Path) -> FastAPI:
    app = FastAPI()
    app.include_router(api)
    app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
    app.add_exception_handler(
        WalletNotFoundException, wallet_not_found_exception_handler
    )
    app.add_exception_handler(NotAuthorizedException, not_authorized_exception_handler)
    app.add_exception_handler(ForbiddenException, forbidden_access_exception_handler)
    app.add_exception_handler(
        NotEnoughBitcoinsException, not_enough_bitcoins_exception_handler
    )
    app.add_exception_handler(
        UserReachedWalletLimitException, user_reached_wallet_limit_exception_handler
    )

    db = SqliteDbInitializer(script, str(db_path))
    wallet_rep = SqlWalletRepository(db.get_connection())
    statistics_rep = SqlStatisticRepository(db.get_connection())
    transaction_rep = SqlTransactionRepository(db.get_connection())
    user_rep = SqlUserRepository(db.get_connection())
    encoder = SimpleKeyEncoder()

    app.state.core = BitcoinService(
        StatisticInteractor(statistics_rep),
        WalletInteractor(wallet_rep),
        TransactionsInteractor(transaction_rep, wallet_rep),
        UserInteractor(user_rep),
        CexBitcoinConverter(),
        SimpleAuth(user_rep, encoder),
    )
    return app
