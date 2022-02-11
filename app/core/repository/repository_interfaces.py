from typing import Protocol, Optional, List

from app.core.models.statistic import Statistics
from app.core.models.transaction import Transaction
from app.core.models.user import User
from app.core.models.wallet import Wallet


class IUserRepository(Protocol):
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    def add(self, user: User) -> User:
        pass


class IWalletRepository(Protocol):
    def get_by_address(self, wallet_address: int) -> Optional[Wallet]:
        pass

    def update_wallet_balance(self, wallet_address: int, balance_btc: float) -> None:
        pass

    def add(self, wallet: Wallet) -> None:
        pass


class ITransactionRepository(Protocol):
    def get_transactions_by_wallet_address(
        self, wallet_address: int
    ) -> List[Transaction]:
        pass

    def get_transactions_by_user_id(self, user_id: int) -> List[Transaction]:
        pass

    def add(self, transaction: Transaction) -> None:
        pass


class IStatisticRepository(Protocol):
    def get(self) -> Statistics:
        pass

    def update(self, num_transactions: int, amount: float) -> None:
        pass
