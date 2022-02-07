import sqlite3
from dataclasses import dataclass
from typing import List, Set

from app.core.models.transaction import Transaction
from app.core.repository.repository_interfaces import ITransactionRepository


class SqlTransactionRepository(ITransactionRepository):
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def get_transactions_by_user_id(self, user_id: int) -> List[Transaction]:
        res_list: List[Transaction] = []
        res_set: Set[int] = set()
        get_user_wallets = "SELECT wallet_address FROM wallet_table WHERE user_id = ?"
        self.cursor.execute(get_user_wallets, [user_id])
        user_wallets = self.cursor.fetchall()

        for wallet_address in user_wallets:
            curr_wallet_transactions = self.get_transactions_by_wallet_address(
                wallet_address[0]
            )
            for curr_trans in curr_wallet_transactions:
                if not res_set.__contains__(curr_trans.transaction_id):
                    res_list.append(curr_trans)
                    res_set.add(curr_trans.transaction_id)

        return res_list

    def get_transactions_by_wallet_address(
        self, wallet_address: int
    ) -> List[Transaction]:
        res_list: List[Transaction] = []

        get_from_wallet_address = (
            "SELECT from_wallet_address, to_wallet_address, bitcoin_quantity,"
            " fee, transaction_id  FROM transaction_table WHERE from_wallet_address = ? "
        )
        self.cursor.execute(get_from_wallet_address, [wallet_address])
        from_wallet = self.cursor.fetchall()

        for trans in from_wallet:
            res_list.append(
                Transaction(trans[0], trans[1], trans[2], trans[3], trans[4])
            )

        get_to_wallet_address = (
            "SELECT from_wallet_address, to_wallet_address, bitcoin_quantity, fee, transaction_id"
            " FROM transaction_table WHERE to_wallet_address = ? AND "
            " to_wallet_address != from_wallet_address"
        )
        self.cursor.execute(get_to_wallet_address, [wallet_address])
        to_wallet = self.cursor.fetchall()

        for trans in to_wallet:
            res_list.append(
                Transaction(trans[0], trans[1], trans[2], trans[3], trans[4])
            )

        return res_list

    def add(self, transactions: Transaction) -> None:

        from_wallet_address = transactions.from_address
        to_wallet_address = transactions.to_address
        bitcoin_quantity = transactions.amount
        fee = transactions.fee
        add_transaction = (
            "INSERT INTO transaction_table(from_wallet_address, to_wallet_address, bitcoin_quantity, "
            "fee) VALUES(?, ?, ?, ?) "
        )
        self.cursor.execute(
            add_transaction,
            [from_wallet_address, to_wallet_address, bitcoin_quantity, fee],
        )
