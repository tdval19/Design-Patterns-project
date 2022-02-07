from dataclasses import dataclass
from typing import List

from app.core.models.transaction import Transaction


@dataclass
class Wallet:
    wallet_id: int
    user_id: int
    balance_btc: float
