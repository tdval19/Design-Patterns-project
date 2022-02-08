import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection

from app.core.models.statistic import Statistics
from app.core.repository.repository_interfaces import IStatisticRepository


@dataclass
class SqlStatisticRepository(IStatisticRepository):
    con: Connection

    def get(self) -> Statistics:
        statement = "SELECT * FROM  statistics_table"
        cursor = self.con.cursor()
        cursor.execute(statement)
        rows = cursor.fetchall()
        cursor.close()
        total_profit = rows[0][0]
        total_transactions = rows[0][1]
        return Statistics(total_transactions, total_profit)

    def update(self, num_transactions: int, amount: float) -> None:
        old_stats = self.get()
        old_stats.num_of_transactions += num_transactions
        old_stats.total_profit += amount

        cursor = self.con.cursor()
        statement = (
            "UPDATE statistics_table SET total_profit = ?, total_transactions = ?"
        )
        cursor.execute(
            statement, (old_stats.total_profit, old_stats.num_of_transactions)
        )
        self.con.commit()
        cursor.close()
