from dataclasses import dataclass
from typing import Optional

from app.core.models.wallet import Wallet


@dataclass
class WalletInteractor:
    def get_wallets(self, user_id: int, address: int) -> Optional[Wallet]:
        pass

    def create_wallet(self, user_id: int) -> Optional[Wallet]:
        pass
