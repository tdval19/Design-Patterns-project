from dataclasses import dataclass
from typing import Optional

from app.core.models.wallet import Wallet
from app.core.repository.repository_interfaces import IWalletRepository


@dataclass
class SqlWalletRepository(IWalletRepository):
    db_name: str

    def get_by_address(self, wallet_address: int) -> Optional[Wallet]:
        pass

    def update_wallet_balance(self) -> None:
        pass

    def add(self, wallet: Wallet) -> None:
        pass
