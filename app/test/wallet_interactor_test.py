import sqlite3
from pathlib import Path
from app.test.db_path_fixture import get_db_script_path
import pytest

from app.core.interactors.wallets import WalletInteractor, UserReachedWalletLimitException, WalletNotFoundException
from app.infra.db.init_db import SqliteDbInitializer
from app.infra.db.rep.wallet_repository import SqlWalletRepository


@pytest.fixture
def connection(get_db_script_path: Path) -> sqlite3.Connection:
    db = SqliteDbInitializer(get_db_script_path, ":memory:")
    connection = db.get_connection()
    return connection


class TestWalletInteractor:

    def test_create_wallet(self, connection: sqlite3.Connection) -> None:
        wallet_repository = SqlWalletRepository(connection)
        wallet_interactor = WalletInteractor(wallet_repository)
        new_wallet = wallet_interactor.create_wallet(1)
        get_wallets = wallet_repository.get_wallets_by_user_id(new_wallet.wallet_address)
        assert get_wallets.__contains__(new_wallet)

    def test_get_wallet(self, connection: sqlite3.Connection) -> None:
        wallet_repository = SqlWalletRepository(connection)
        wallet_interactor = WalletInteractor(wallet_repository)
        new_wallet = wallet_interactor.create_wallet(1)
        get_wallet = wallet_interactor.get_wallet(new_wallet.wallet_address)
        wallets_from_repository = wallet_repository.get_wallets_by_user_id(new_wallet.wallet_address)
        assert wallets_from_repository.__contains__(get_wallet)

    def test_four_wallets(self, connection: sqlite3.Connection) -> None:
        wallet_repository = SqlWalletRepository(connection)
        wallet_interactor = WalletInteractor(wallet_repository)
        for i in range(0, 3):
            new_wallet = wallet_interactor.create_wallet(1)
        with pytest.raises(UserReachedWalletLimitException):
            new_wallet = wallet_interactor.create_wallet(1)

    def test_undefined_wallet(self, connection: sqlite3.Connection) -> None:
        wallet_repository = SqlWalletRepository(connection)
        wallet_interactor = WalletInteractor(wallet_repository)
        with pytest.raises(WalletNotFoundException):
            get_wallet = wallet_interactor.get_wallet(-1)

