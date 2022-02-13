from dataclasses import dataclass

from app.core.models.wallet import Wallet
from app.core.repository.repository_interfaces import IWalletRepository


@dataclass
class WalletInteractor:
    repository: IWalletRepository
    num_wallet_limit: int = 3
    initial_balance_btc: int = 1

    def get_wallet(self, address: int) -> Wallet:
        result_wallet = self.repository.get_by_address(address)
        if result_wallet is None:
            raise WalletNotFoundException(address)
        return result_wallet

    def create_wallet(self, user_id: int) -> Wallet:
        user_wallets = self.repository.get_wallets_by_user_id(user_id)
        if len(user_wallets) >= self.num_wallet_limit:
            raise UserReachedWalletLimitException(user_id)
        add_wallet = Wallet(user_id, self.initial_balance_btc)
        return self.repository.add(add_wallet)


class UserReachedWalletLimitException(Exception):
    def __init__(self, user_id: int):
        self.message = "User with ID {} reached wallet limit".format(user_id)


class WalletNotFoundException(Exception):
    def __init__(self, address: int):
        self.message = "Wallet with address {} not found".format(address)
