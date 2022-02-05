import sqlite3
from dataclasses import dataclass

from app.core.models.statistic import Statistics
from app.core.repository.repository_interfaces import IStatisticRepository


@dataclass
class SqlStatisticRepository(IStatisticRepository):
    db_name: str

    def get(self) -> Statistics:
        con = sqlite3.connect(self.db_name)
        statement = "SELECT * FROM  statistics_table"
        cursor = con.cursor()
        cursor.execute(statement)
        rows = cursor.fetchall()
        total_profit = rows[0][0]
        total_transactions = rows[0][1]
        return Statistics(total_transactions, total_profit)

    def update(self, num_transactions: int, amount: float) -> None:
        old_stats = self.get()
        old_stats.num_of_transactions += num_transactions
        old_stats.total_profit += amount

        con = sqlite3.connect(self.db_name)
        cursor = con.cursor()
        statement = "UPDATE statistics_table SET total_profit = ?, total_transactions = ?"
        cursor.execute(statement, (old_stats.total_profit, old_stats.num_of_transactions))
