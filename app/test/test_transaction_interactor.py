import sqlite3
from pathlib import Path

import pytest

from app.core.interactors.transactions import (
    TransactionsInteractor,
    NotEnoughBitcoinsException,
)
from app.core.models.transaction import Transaction
from app.core.models.wallet import Wallet
from app.infra.db.init_db import SqliteDbInitializer
from app.infra.db.rep.transaction_repository import SqlTransactionRepository
from app.infra.db.rep.wallet_repository import SqlWalletRepository
from app.test.db_path_fixture import get_db_script_path


@pytest.fixture
def connection(get_db_script_path: Path) -> sqlite3.Connection:
    db = SqliteDbInitializer(get_db_script_path, ":memory:")
    connection = db.get_connection()
    return connection


class TestTransactionsInteractor:
    def test_make_transaction_get_by_wallet_id_single_transaction(
        self, connection: sqlite3.Connection
    ) -> None:
        transaction_repository = SqlTransactionRepository(connection)
        wallet_repository = SqlWalletRepository(connection)
        get_wallet_from = wallet_repository.add(Wallet(1, 5.00))
        get_wallet_to = wallet_repository.add(Wallet(2, 7.50))
        transaction_interactor = TransactionsInteractor(
            transaction_repository, wallet_repository
        )
        transaction = Transaction(
            get_wallet_from.wallet_address, get_wallet_to.wallet_address, 2.00, 0.5, 1
        )
        transaction_interactor.make_transaction(
            transaction, get_wallet_from, get_wallet_to
        )
        from_test = transaction_interactor.get_wallet_transactions(
            get_wallet_from.wallet_address
        )
        to_test = transaction_interactor.get_wallet_transactions(
            get_wallet_to.wallet_address
        )
        assert from_test[0] == transaction
        assert to_test[0] == transaction

    def test_make_transaction_get_by_wallet_id_multiple_transaction(
        self, connection: sqlite3.Connection
    ) -> None:
        transaction_repository = SqlTransactionRepository(connection)
        wallet_repository = SqlWalletRepository(connection)
        get_wallet_from = wallet_repository.add(Wallet(1, 10.00))
        get_wallet_to = wallet_repository.add(Wallet(2, 15.50))
        transaction_interactor = TransactionsInteractor(
            transaction_repository, wallet_repository
        )
        transaction_one = Transaction(
            get_wallet_from.wallet_address, get_wallet_to.wallet_address, 3.5, 2.5, 1
        )
        transaction_two = Transaction(
            get_wallet_from.wallet_address, get_wallet_to.wallet_address, 1.5, 2.00, 2
        )
        transaction_interactor.make_transaction(
            transaction_one, get_wallet_from, get_wallet_to
        )
        transaction_interactor.make_transaction(
            transaction_two, get_wallet_from, get_wallet_to
        )
        from_test = transaction_interactor.get_wallet_transactions(
            get_wallet_from.wallet_address
        )
        assert from_test[0] == transaction_one
        assert from_test[1] == transaction_two

    def test_not_enough_bitcoins(self, connection: sqlite3.Connection) -> None:
        transaction_repository = SqlTransactionRepository(connection)
        wallet_repository = SqlWalletRepository(connection)
        get_wallet_from = wallet_repository.add(Wallet(1, 10.00))
        get_wallet_to = wallet_repository.add(Wallet(2, 15.50))
        transaction_interactor = TransactionsInteractor(
            transaction_repository, wallet_repository
        )
        transaction = Transaction(
            get_wallet_from.wallet_address,
            get_wallet_to.wallet_address,
            100.00,
            10.00,
            1,
        )
        with pytest.raises(NotEnoughBitcoinsException):
            transaction_interactor.make_transaction(
                transaction, get_wallet_from, get_wallet_to
            )
