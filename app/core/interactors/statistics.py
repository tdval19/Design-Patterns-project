from dataclasses import dataclass
from app.core.models.statistic import Statistics
from app.core.repository.repository_interfaces import IStatisticRepository


@dataclass
class StatisticInteractor:
    statistics_repository: IStatisticRepository

    def get_statistics(self) -> Statistics:
        return self.statistics_repository.get()

    def update_statistics(
        self, change_in_num_transactions: int, change_in_amount: float
    ) -> None:
        self.statistics_repository.update(change_in_num_transactions, change_in_amount)
