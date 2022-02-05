from dataclasses import dataclass
from typing import Optional
from app.core.models.statistic import Statistics
from app.core.repository.statistics_rep import IStatisticRepository


@dataclass
class StatisticInteractor:
    statistics_repository: IStatisticRepository

    def get_statistics(self, admin_key: int) -> Optional[Statistics]:
        return self.statistics_repository.get()

    def update_statistics(self, num_transactions: int, amount: float) -> None:
        self.statistics_repository.update(num_transactions, amount)
        
