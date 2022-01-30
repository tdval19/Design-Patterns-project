from dataclasses import dataclass
from typing import Optional, List

from app.core.interactors.admin import AdminInteractor
from app.core.interactors.transactions import TransactionsInteractor
from app.core.interactors.users import UserInteractor
from app.core.interactors.wallets import WalletInteractor
from app.core.models.statistics import Statistics
from app.core.models.transaction import Transaction
from app.core.models.user import User
from app.core.models.wallet import Wallet


@dataclass
class BitcoinService:
    admin_interactor: AdminInteractor
    wallet_interactor: WalletInteractor
    transaction_interactor: TransactionsInteractor
    user_interactor: UserInteractor

    #wallet_interactor
    def get_wallets(self, user_id: int, address: int) -> Optional[Wallet]:
        return self.wallet_interactor.get_wallets(user_id, address)

    def create_wallet(self, user_id: int) -> Optional[Wallet]:
        return self.wallet_interactor.create_wallet(user_id)

    #transactions_interactor
    def get_wallet_transactions(self, user_id: int, address: int) -> Optional[List[Transaction]]:
        return self.transaction_interactor.get_wallet_transactions(user_id, address)

    def get_transactions(self, user_id: int) -> Optional[List[Transaction]]:
        return self.transaction_interactor.get_transactions(user_id)

    def make_transaction(self, user_id: int, transaction: Transaction) -> bool:
        return self.transaction_interactor.make_transaction(user_id, transaction)

    #user_interactor
    def create_user(self) -> Optional[User]:
        return self.user_interactor.create_user()

    #admin_interactor
    def get_statistics(self, admin_key: int) -> Optional[Statistics]:
        return self.admin_interactor.get_statistics(admin_key)




