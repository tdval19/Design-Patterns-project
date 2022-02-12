from dataclasses import dataclass
from typing import Optional, List
from app.core.converter.bitcoin_converter import IBitcoinConverter
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

    # wallet_interactor
    def get_wallet(self, address: int) -> Wallet:
        return self.wallet_interactor.get_wallet(address)

    def create_wallet(self, user_id: int) -> Wallet:
        return self.wallet_interactor.create_wallet(user_id)

    # transactions_interactor
    def get_wallet_transactions(self, address: int) -> List[Transaction]:
        wallet = self.wallet_interactor.get_wallet(address)
        return self.transaction_interactor.get_wallet_transactions(
            wallet.wallet_address
        )

    def get_user_transactions(self, user_id: int) -> List[Transaction]:
        user = self.user_interactor.get_user(user_id)
        return self.transaction_interactor.get_user_transactions(user.user_id)

    def make_transaction(self, transaction: Transaction) -> None:
        to_wallet = self.wallet_interactor.get_wallet(transaction.to_address)
        from_wallet = self.wallet_interactor.get_wallet(transaction.from_address)
        self.transaction_interactor.make_transaction(
            transaction, from_wallet, to_wallet
        )

    # user_interactor
    def create_user(self) -> User:
        return self.user_interactor.create_user()

    def get_user(self, user_id: int) -> User:
        return self.user_interactor.get_user(user_id)

    # admin_interactor
    def get_statistics(self, key: str) -> Statistics:
        return self.statistic_interactor.get_statistics()

    # bitcoin_converter
    def convert_bitcoin_to(self, currency: str, amount_btc: float) -> Optional[float]:
        return self.bitcoin_converter.convert_btc_to(currency, amount_btc)
