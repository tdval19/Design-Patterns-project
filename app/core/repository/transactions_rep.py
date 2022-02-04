import sqlite3
from typing import Protocol, List
from app.core.models import transaction


class ITransactionRepository(Protocol):

    def get_user_transactions(self, user_id: int) -> List[transaction.Transaction]:
        pass

    def get_wallet_transactions(self, user_id: int, wallet_address: int) -> List[transaction.Transaction]:
        pass

    def make_transfer(self, user_id: int, trans: transaction.Transaction) -> bool:
        pass


class TransactionRepository(ITransactionRepository):

    def __init__(self):
        self.connection = sqlite3.connect('project_db')
        self.cursor = self.connection.cursor()

    def get_user_transactions(self, user_id: int) -> List[transaction.Transaction]:
        res_list: List[transaction.Transaction] = []
        get_user_wallets = "SELECT wallet_address FROM wallet_table WHERE user_id = ?"
        self.cursor.execute(get_user_wallets, [user_id])
        user_wallets = self.cursor.fetchall()

        for wallet_address in user_wallets:
            curr_wallet_transactions = self.get_wallet_transactions(user_id, wallet_address)
            res_list.extend(curr_wallet_transactions)

        return res_list

    def get_wallet_transactions(self,  user_id: int, wallet_address: int) -> List[transaction.Transaction]:
        res_list: List[transaction.Transaction] = []

        get_from_wallet_address = "SELECT from_wallet_address, to_wallet_address, bitcoin_quantity, fee  FROM " \
                                  "transaction_table WHERE from_wallet_address = ? "
        self.cursor.execute(get_from_wallet_address, [wallet_address])
        from_wallet = self.cursor.fetchall()

        for trans in from_wallet:
            res_list.append(transaction.Transaction(trans[0], trans[1], trans[2], trans[3]))

        get_to_wallet_address = "SELECT from_wallet_address, to_wallet_address, bitcoin_quantity, fee FROM " \
                                "transaction_table WHERE to_wallet_address = ? "
        self.cursor.execute(get_to_wallet_address, [wallet_address])
        to_wallet = self.cursor.fetchall()

        for trans in to_wallet:
            res_list.append(transaction.Transaction(trans[0], trans[1], trans[2], trans[3]))

        return res_list

    def make_transfer(self, user_id: int, trans: transaction.Transaction) -> bool:

        from_wallet_address = trans.from_address
        to_wallet_address = trans.to_address
        bitcoin_quantity = trans.amount
        fee = trans.fee
        add_transaction = "INSERT INTO transaction_table(from_wallet_address, to_wallet_address, bitcoin_quantity, " \
                          "fee) VALUES(?, ?, ?, ?) "
        self.cursor.execute(add_transaction, [from_wallet_address, to_wallet_address, bitcoin_quantity, fee])
        return True
