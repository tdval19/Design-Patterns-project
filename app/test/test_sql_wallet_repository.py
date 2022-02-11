from pathlib import Path

import pytest

from app.core.models.wallet import Wallet
from app.infra.db.init_db import SqliteDbInitializer
from app.infra.db.rep.wallet_repository import SqlWalletRepository
from app.test.db_path_fixture import get_db_script_path


@pytest.fixture
def repository(get_db_script_path: Path) -> SqlWalletRepository:
    db = SqliteDbInitializer(get_db_script_path, ":memory:")
    return SqlWalletRepository(db.get_connection())


class TestSqlWalletRepository:
    def test_add_get_by_address(self, repository: SqlWalletRepository) -> None:
        wallet = Wallet(1, 5.12, 2)
        repository.add(wallet)
        get_wallet = repository.get_by_address(2)
        assert wallet == get_wallet
        wallet = Wallet(5, 136.7, 3)
        repository.add(wallet)
        get_wallet = repository.get_by_address(3)
        assert wallet == get_wallet

    def test_update_balance(self, repository: SqlWalletRepository) -> None:
        wallet = Wallet(5, 100, 10)
        repository.add(wallet)
        get_wallet = repository.get_by_address(10)
        assert wallet == get_wallet
        repository.update_wallet_balance(10, 200)
        expected_wallet = Wallet(5, 200, 10)
        assert repository.get_by_address(10) == expected_wallet

