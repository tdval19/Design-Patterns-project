from pathlib import Path

import pytest

from app.core.models.transaction import Transaction
from app.infra.db.init_db import SqliteDbInitializer
from app.infra.db.rep.transaction_repository import SqlTransactionRepository
from app.test.db_path_fixture import get_db_script_path


@pytest.fixture
def repository(get_db_script_path: Path) -> SqlTransactionRepository:
    db = SqliteDbInitializer(get_db_script_path, ":memory:")
    return SqlTransactionRepository(db.get_connection())


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
        assert transaction_list_one[0] == transaction_one
        assert transaction_list_one[1] == transaction_two
        assert transaction_list_one[2] == transaction_three
        assert transaction_list_two[0] == transaction_three
        assert transaction_list_two[1] == transaction_one
        assert transaction_list_three[0] == transaction_four
        assert transaction_list_four[0] == transaction_four
