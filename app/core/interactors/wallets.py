from dataclasses import dataclass
from typing import Optional

from app.core.models.wallet import Wallet
from app.core.repository.repository_interfaces import IWalletRepository


@dataclass
class WalletInteractor:
    repository: IWalletRepository

    def get_wallet(self, address: int) -> Optional[Wallet]:
        pass

    def create_wallet(self, user_id: int) -> Wallet:
        pass
