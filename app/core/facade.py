from dataclasses import dataclass, field
from typing import Optional, List
from app.core.converter.bitcoin_converter import IBitcoinConverter
from app.core.interactors.auth import IUserAuth, UserCredentials
from app.core.interactors.statistics import StatisticInteractor
from app.core.interactors.transactions import TransactionsInteractor
from app.core.interactors.users import UserInteractor
from app.core.interactors.wallets import WalletInteractor
from app.core.models.statistic import Statistics
from app.core.models.transaction import Transaction
from app.core.models.user import User
from app.core.models.wallet import Wallet


@dataclass
class BitcoinService:
    statistic_interactor: StatisticInteractor
    wallet_interactor: WalletInteractor
    transaction_interactor: TransactionsInteractor
    user_interactor: UserInteractor
    bitcoin_converter: IBitcoinConverter
    auth: IUserAuth

    def get_wallet(self, key: Optional[str], address: int) -> Wallet:
        self.auth.authorize_user(key)
        wallet = self.wallet_interactor.get_wallet(address)
        self.auth.user_has_permission(key, wallet.user_id)
        return wallet

    def create_wallet(self, key: Optional[str]) -> Wallet:
        credentials = self.auth.authorize_user(key)
        return self.wallet_interactor.create_wallet(credentials.user_id)

    def get_wallet_transactions(
        self, key: Optional[str], address: int
    ) -> List[Transaction]:
        self.auth.authorize_user(key)
        wallet = self.wallet_interactor.get_wallet(address)
        self.auth.user_has_permission(key, wallet.user_id)
        return self.transaction_interactor.get_wallet_transactions(
            wallet.wallet_address
        )

    def get_user_transactions(self, key: Optional[str]) -> List[Transaction]:
        credentials = self.auth.authorize_user(key)
        user = self.user_interactor.get_user(credentials.user_id)
        return self.transaction_interactor.get_user_transactions(user.user_id)

    def make_transaction(self, key: Optional[str], transaction: Transaction) -> None:
        self.auth.authorize_user(key)
        from_wallet = self.wallet_interactor.get_wallet(transaction.from_address)
        self.auth.user_has_permission(key, from_wallet.user_id)
        to_wallet = self.wallet_interactor.get_wallet(transaction.to_address)
        self.transaction_interactor.make_transaction(
            transaction, from_wallet, to_wallet
        )

    # user_interactor
    def create_user(self) -> str:
        user = self.user_interactor.create_user()
        credentials = UserCredentials(user.user_id)
        return self.auth.generate_key(credentials)

    # admin_interactor
    def get_statistics(self, key: Optional[str]) -> Statistics:
        self.auth.authorize_admin(key)
        return self.statistic_interactor.get_statistics()

    # bitcoin_converter
    def convert_bitcoin_to(self, currency: str, amount_btc: float) -> Optional[float]:
        return self.bitcoin_converter.convert_btc_to(currency, amount_btc)