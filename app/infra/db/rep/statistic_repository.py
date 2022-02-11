from dataclasses import dataclass
from sqlite3 import Connection

from app.core.models.statistic import Statistics
from app.core.repository.repository_interfaces import IStatisticRepository


@dataclass
class SqlStatisticRepository(IStatisticRepository):
    con: Connection

    def get(self) -> Statistics:
        statement = "SELECT fee FROM transaction_table"
        cursor = self.con.cursor()
        cursor.execute(statement)
        rows = cursor.fetchall()
        cursor.close()
        total_transactions = 0
        total_profit = 0
        for row in rows:
            total_transactions += 1
            total_profit += row[0]
        return Statistics(total_transactions, total_profit)
