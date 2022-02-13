from pathlib import Path
from sqlite3 import Connection

import pytest

from app.core.models.transaction import Transaction
from app.core.models.wallet import Wallet
from app.infra.db.init_db import SqliteDbInitializer
from app.infra.db.rep.transaction_repository import SqlTransactionRepository
from app.infra.db.rep.wallet_repository import SqlWalletRepository
from app.test.db_path_fixture import get_db_script_path


@pytest.fixture
def db_fixture(get_db_script_path: Path) -> Connection:
    db = SqliteDbInitializer(get_db_script_path, ":memory:")
    return db.get_connection()


@pytest.fixture
def repository(db_fixture: Connection) -> SqlTransactionRepository:
    return SqlTransactionRepository(db_fixture)


@pytest.fixture
def wallet_repository(db_fixture: Connection) -> SqlWalletRepository:
    return SqlWalletRepository(db_fixture)


class TestSqlTransactionRepository:
    def test_add_get_by_wallet_different_account(
        self, repository: SqlTransactionRepository
    ) -> None:
        transaction = Transaction(1, 2, 1.00, 1.5, 1)
        repository.add(transaction)
        transaction_list_from = repository.get_transactions_by_wallet_address(1)
        transaction_list_to = repository.get_transactions_by_wallet_address(2)
        assert len(transaction_list_from) == len(transaction_list_to) == 1
        assert transaction_list_from[0] == transaction_list_to[0] == transaction

    def test_add_get_by_wallet_same_account(
        self, repository: SqlTransactionRepository
    ) -> None:
        transaction = Transaction(1, 1, 500, 2.00, 1)
        repository.add(transaction)
        transaction_list = repository.get_transactions_by_wallet_address(1)
        assert len(transaction_list) == 1
        assert transaction_list[0] == transaction

    def test_add_get_by_wallet_multiple_transactions(
        self, repository: SqlTransactionRepository
    ) -> None:
        transaction_one = Transaction(1, 2, 1.00, 1.5, 1)
        transaction_two = Transaction(1, 1, 500, 2.00, 2)
        transaction_three = Transaction(2, 1, 666, 5.00, 3)
        transaction_four = Transaction(4, 3, 10, 3.00, 4)
        repository.add(transaction_one)
        repository.add(transaction_two)
        repository.add(transaction_three)
        repository.add(transaction_four)
        transaction_list_one = repository.get_transactions_by_wallet_address(1)
        transaction_list_two = repository.get_transactions_by_wallet_address(2)
        transaction_list_three = repository.get_transactions_by_wallet_address(3)
        transaction_list_four = repository.get_transactions_by_wallet_address(4)
        assert len(transaction_list_one) == 3
        assert len(transaction_list_two) == 2
        assert len(transaction_list_three) == 1
        assert len(transaction_list_four) == 1
        assert (
            transaction_list_one.count(transaction_one) > 0
            and transaction_list_one.count(transaction_two) > 0
            and transaction_list_one.count(transaction_three) > 0
        )
        assert (
            transaction_list_two.count(transaction_one) > 0
            and transaction_list_one.count(transaction_three) > 0
        )
        assert transaction_list_three.count(transaction_four) > 0
        assert transaction_list_four.count(transaction_four) > 0

    def test_get_by_user_id_single(
        self,
        repository: SqlTransactionRepository,
        wallet_repository: SqlWalletRepository,
    ) -> None:
        from_wallet = wallet_repository.add(Wallet(1, 5.00))
        to_wallet = wallet_repository.add(Wallet(2, 7.00))
        transaction = Transaction(
            from_wallet.wallet_address, to_wallet.wallet_address, 2.00, 0.5, 1
        )
        repository.add(transaction)
        from_user_trans = repository.get_transactions_by_user_id(from_wallet.user_id)
        to_user_trans = repository.get_transactions_by_user_id(to_wallet.user_id)
        assert from_user_trans[0] == to_user_trans[0] == transaction

    def test_get_by_user_id_multiple(
        self,
        repository: SqlTransactionRepository,
        wallet_repository: SqlWalletRepository,
    ) -> None:
        from_wallet = wallet_repository.add(Wallet(1, 100))
        to_wallet = wallet_repository.add(Wallet(2, 50.00))
        transaction_one = Transaction(
            from_wallet.wallet_address, to_wallet.wallet_address, 10.50, 0.5, 1
        )
        transaction_two = Transaction(
            to_wallet.wallet_address, from_wallet.wallet_address, 20.00, 0.5, 2
        )
        transaction_three = Transaction(
            from_wallet.wallet_address, to_wallet.wallet_address, 5.50, 3.00, 3
        )
        repository.add(transaction_one)
        repository.add(transaction_two)
        repository.add(transaction_three)
        from_user_trans = repository.get_transactions_by_user_id(from_wallet.user_id)
        to_user_trans = repository.get_transactions_by_user_id(to_wallet.user_id)
        assert (
            from_user_trans.count(transaction_one) > 0
            and from_user_trans.count(transaction_two) > 0
            and from_user_trans.count(transaction_three) > 0
        )
        assert (
            to_user_trans.count(transaction_one) > 0
            and from_user_trans.count(transaction_two) > 0
            and from_user_trans.count(transaction_three) > 0
        )
