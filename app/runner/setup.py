from fastapi import FastAPI

from app.core.converter.bitcoin_converter import CexBitcoinConverter
from app.core.facade import BitcoinService
from app.core.interactors.admin import AdminInteractor
from app.core.interactors.transactions import TransactionsInteractor
from app.core.interactors.users import UserInteractor
from app.core.interactors.wallets import WalletInteractor
from app.infra.fastapi.test import api


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(api)
    app.state.core = BitcoinService(
        AdminInteractor(),
        WalletInteractor(),
        TransactionsInteractor(),
        UserInteractor(),
    )
    app.state.converter = CexBitcoinConverter()
    return app
