from dataclasses import dataclass
from typing import Optional

from app.core.models.statistics import Statistics


@dataclass
class AdminInteractor:
    def get_statistics(self, admin_key: int) -> Optional[Statistics]:
        pass
