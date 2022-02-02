from dataclasses import dataclass
from typing import Optional
from app.core.models.statistics import Statistics
from app.core.repository import statistics_rep


@dataclass
class AdminInteractor:
    statistics_repository: statistics_rep.IStatisticRepository

    def get_statistics(self, admin_key: int) -> Optional[Statistics]:
        if self.statistics_repository.is_admin(admin_key):
            return self.statistics_repository.get_statistics()
        else:
            return None

    def update_statistics(self, num_transactions: int, amount: float) -> None:
        pass
        
