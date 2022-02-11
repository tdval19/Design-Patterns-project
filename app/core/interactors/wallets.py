from dataclasses import dataclass
from typing import Optional

from app.core.models.wallet import Wallet
from app.core.repository.repository_interfaces import IWalletRepository


@dataclass
class WalletInteractor:
    repository: IWalletRepository

    def get_wallet(self, address: int) -> Wallet:
        result_wallet = self.repository.get_by_address(address)
        if result_wallet is None:
            raise WalletNotFoundException(address)
        return result_wallet

    def create_wallet(self, user_id: int) -> Wallet:
        user_wallets = self.repository.get_wallets_by_user_id(user_id)
        if len(user_wallets) >= 3:
            raise UserReachedWalletLimitException(user_id)
        add_wallet = Wallet(user_id, 1.0)
        return self.repository.add(add_wallet)


class UserReachedWalletLimitException(Exception):
    def __init__(self, user_id: int):
        self.message = "User with ID {} reached wallet limit".format(user_id)


class WalletNotFoundException(Exception):
    def __init__(self, address: int):
        self.message = "Wallet with address {} not found".format(address)
