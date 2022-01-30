from dataclasses import dataclass
from typing import Optional, List

from app.core.models.transaction import Transaction


@dataclass
class TransactionsInteractor:

    def get_wallet_transactions(self, user_id: int, address: int) -> Optional[List[Transaction]]:
        pass

    def get_transactions(self, user_id: int) -> Optional[List[Transaction]]:
        pass

    def make_transaction(self, user_id: int, transaction: Transaction) -> bool:
        pass
