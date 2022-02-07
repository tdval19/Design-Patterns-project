from dataclasses import dataclass
from typing import Optional, List
from app.core.models.transaction import Transaction
from app.core.repository.repository_interfaces import ITransactionRepository


@dataclass
class TransactionsInteractor:
    transaction_repository: ITransactionRepository

    def get_wallet_transactions(
        self, user_id: int, address: int
    ) -> Optional[List[Transaction]]:
        return self.transaction_repository.get_transactions_by_wallet_address(address)

    def get_user_transactions(self, user_id: int) -> Optional[List[Transaction]]:
        return self.transaction_repository.get_transactions_by_user_id(user_id)

    def transfer(self, user_id: int, transaction: Transaction) -> None:
        self.transaction_repository.add(transaction)
