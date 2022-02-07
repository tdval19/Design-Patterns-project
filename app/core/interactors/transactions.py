from dataclasses import dataclass
from typing import Optional, List
from app.core.repository import transactions_rep
from app.core.models.transaction import Transaction


@dataclass
class TransactionsInteractor:
    transaction_repository: transactions_rep.ITransactionRepository

    def get_wallet_transactions(
        self, user_id: int, address: int
    ) -> Optional[List[Transaction]]:
        return self.transaction_repository.get_wallet_transactions(user_id, address)

    def get_user_transactions(self, user_id: int) -> Optional[List[Transaction]]:
        return self.transaction_repository.get_user_transactions(user_id)

    def transfer(self, user_id: int, transaction: Transaction) -> bool:
        return self.transaction_repository.make_transfer(user_id, transaction)
