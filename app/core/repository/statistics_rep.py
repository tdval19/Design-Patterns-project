import sqlite3
from dataclasses import dataclass
from typing import Protocol
from app.core.models import statistics

ADMIN_KEY = 0


class IStatisticRepository(Protocol):
    def get_statistics(self) -> statistics.Statistics:
        pass

    def is_admin(self, api_key: int) -> bool:
        pass


class StatisticsDBRepository(IStatisticRepository):

    def __init__(self) -> None:
        self.connection = sqlite3.connect('project_db')
        self.cursor = self.connection.cursor()

    def get_statistics(self) -> statistics.Statistics:
        statement = "SELECT from_wallet_address, to_wallet_address, bitcoin_quantity FROM transaction_table"
        self.cursor.execute(statement)
        rows = self.cursor.fetchall()
        num_transactions = len(rows)
        profit_bitcoins = 0.0
        for row in rows:
            from_address = row[0]
            to_address = row[1]
            bitcoins = row[2]
            if from_address != to_address:
                profit_bitcoins += bitcoins / 100 * 1.5
        return statistics.Statistics(num_transactions, profit_bitcoins)

    def is_admin(self, api_key: int) -> bool:
        return api_key == ADMIN_KEY


class set_up_db_staff:

    def __init__(self) -> None:
        self.connection = sqlite3.connect('project_db')
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        create_user_table = '''CREATE TABLE IF NOT EXISTS user_table(user_id INTEGER PRIMARY KEY AUTOINCREMENT)'''
        self.cursor.execute(create_user_table)

        create_wallet_table = '''CREATE TABLE IF NOT EXISTS wallet_table
                                    (wallet_address INTEGER PRIMARY KEY AUTOINCREMENT, user_id,
                                    FOREIGN KEY (user_id)  REFERENCES user_table (user_id))'''
        self.cursor.execute(create_wallet_table)

        create_transaction_table = ''' CREATE TABLE IF NOT EXISTS transaction_table
                                        (transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        from_wallet_address, to_wallet_address, bitcoin_quantity INTEGER,
                                        FOREIGN KEY (from_wallet_address) REFERENCES wallet_table (wallet_address),
                                        FOREIGN KEY (to_wallet_address) REFERENCES wallet_table (wallet_address))'''
        self.cursor.execute(create_transaction_table)
