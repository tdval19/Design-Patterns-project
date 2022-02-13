from pathlib import Path

import pytest

from app.core.models.wallet import Wallet
from app.infra.db.init_db import SqliteDbInitializer
from app.infra.db.rep.wallet_repository import SqlWalletRepository


@pytest.fixture
def repository(get_db_script_path: Path) -> SqlWalletRepository:
    db = SqliteDbInitializer(get_db_script_path, ":memory:")
    return SqlWalletRepository(db.get_connection())


class TestSqlWalletRepository:
    def test_empty_db(self, repository: SqlWalletRepository) -> None:
        assert repository.get_by_address(1) is None

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

    def test_get_user_wallets(self, repository: SqlWalletRepository) -> None:
        wallet1 = Wallet(1, 5.12)
        wallet2 = Wallet(1, 3.8)
        wallet3 = Wallet(1, 4.9)

        first_added = repository.add(wallet1)
        user_wallets1 = repository.get_wallets_by_user_id(1)
        assert user_wallets1[0] == first_added

        second_added = repository.add(wallet2)
        user_wallets2 = repository.get_wallets_by_user_id(1)
        assert user_wallets2[0] == first_added
        assert user_wallets2[1] == second_added

        third_added = repository.add(wallet3)
        user_wallets3 = repository.get_wallets_by_user_id(1)
        assert user_wallets3[0] == first_added
        assert user_wallets3[1] == second_added
        assert user_wallets3[2] == third_added
