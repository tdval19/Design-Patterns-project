from dataclasses import dataclass, field
from typing import Optional, List
from app.core.models.transaction import Transaction
from app.core.repository.repository_interfaces import ITransactionRepository
from app.core.fee_strategy import IFeeStrategy, StandardFeeStrategy


@dataclass
class TransactionsInteractor:
    transaction_repository: ITransactionRepository
    fee_strategy: IFeeStrategy = field(default_factory=StandardFeeStrategy)

    def get_wallet_transactions(self, address: int) -> List[Transaction]:
        return self.transaction_repository.get_transactions_by_wallet_address(address)

    def get_user_transactions(self, user_id: int) -> List[Transaction]:
        return self.transaction_repository.get_transactions_by_user_id(user_id)

    def add_transaction(
        self, transaction: Transaction, from_user_id: int, to_user_id: int
    ) -> None:
        fee = self.fee_strategy.get_fee(from_user_id, to_user_id, transaction.amount)
        transaction.fee = fee
        self.transaction_repository.add(transaction)
