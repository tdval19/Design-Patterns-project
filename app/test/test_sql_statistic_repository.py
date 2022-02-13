from pathlib import Path
from sqlite3 import Connection

import pytest

from app.core.models.transaction import Transaction
from app.infra.db.init_db import SqliteDbInitializer
from app.infra.db.rep.statistic_repository import SqlStatisticRepository
from app.infra.db.rep.transaction_repository import SqlTransactionRepository


@pytest.fixture
def db_fixture(get_db_script_path: Path) -> Connection:
    db = SqliteDbInitializer(get_db_script_path, ":memory:")
    return db.get_connection()


@pytest.fixture
def repository(db_fixture: Connection) -> SqlStatisticRepository:
    return SqlStatisticRepository(db_fixture)


@pytest.fixture
def transaction_repository(db_fixture: Connection) -> SqlTransactionRepository:
    return SqlTransactionRepository(db_fixture)


class TestSqlStatisticRepository:
    def test_statistic_repository_empty(self, repository: SqlStatisticRepository):
        repository.get().total_profit = 0
        repository.get().num_of_transactions = 0

    def test_statistic_repository_get(self, repository: SqlStatisticRepository,
                                      transaction_repository: SqlTransactionRepository):
        transaction_one = Transaction(1, 2, 5.00, 1.00, 1)
        transaction_two = Transaction(3, 4, 10.50, 2.00, 2)
        transaction_three = Transaction(1, 3, 3.46, 3.50, 3)
        transaction_repository.add(transaction_one)
        transaction_repository.add(transaction_two)
        transaction_repository.add(transaction_three)
        stats = repository.get()
        assert stats.num_of_transactions == 3
        assert stats.total_profit == 6.50
