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
        wallet = Wallet(1, 5.12)
        added_wallet = repository.add(wallet)
        get_wallet = repository.get_by_address(added_wallet.wallet_address)
        assert added_wallet == get_wallet
        wallet = Wallet(5, 136.7)
        added_wallet = repository.add(wallet)
        get_wallet = repository.get_by_address(added_wallet.wallet_address)
        assert added_wallet == get_wallet

    def test_update_balance(self, repository: SqlWalletRepository) -> None:
        wallet = Wallet(5, 100)
        added_wallet = repository.add(wallet)
        get_wallet = repository.get_by_address(added_wallet.wallet_address)
        assert added_wallet == get_wallet
        repository.update_wallet_balance(added_wallet.wallet_address, 200)
        expected_wallet = Wallet(5, 200, added_wallet.wallet_address)
        assert repository.get_by_address(added_wallet.wallet_address) == expected_wallet
