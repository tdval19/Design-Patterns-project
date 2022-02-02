from dataclasses import dataclass
from typing import Protocol


class IFeeStrategy(Protocol):
    def get_fee(self, from_id: int, to_id: int, amount: float) -> float:
        pass


@dataclass
class StandardFeeStrategy(IFeeStrategy):
    fee_for_foreign_wallets_in_percents = 0.015

    def get_fee(self, from_id: int, to_id: int, amount: float) -> float:
        if from_id == to_id:
            return 0
        return self.fee_for_foreign_wallets_in_percents * amount
