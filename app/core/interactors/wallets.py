from dataclasses import dataclass
from typing import Optional

from app.core.models.wallet import Wallet
from app.core.repository.repository_interfaces import IWalletRepository


@dataclass
class WalletInteractor:
    repository: IWalletRepository

    def get_wallet(self, address: int) -> Optional[Wallet]:
        result_wallet = self.repository.get_by_address(address)
        return result_wallet

    def create_wallet(self, user_id: int) -> Wallet:
        user_wallets = self.repository.get_wallets_by_user_id(user_id)
        if len(user_wallets) > 3:
            raise UserRanOutOfWalletLimit
        add_wallet = Wallet(user_id, 1.0)
        return self.repository.add(add_wallet)


class UserRanOutOfWalletLimit(Exception):


    def __init__(self):
        self.message = "User can not have more than three wallets"
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
