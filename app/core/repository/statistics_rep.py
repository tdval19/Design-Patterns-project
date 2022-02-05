import sqlite3
from dataclasses import dataclass
from typing import Protocol
from app.core.models.statistic import Statistics


class IStatisticRepository(Protocol):
    def get (self) -> Statistics:
        pass

    def update(self, num_transactions: int, amount: float) -> None:
        pass



