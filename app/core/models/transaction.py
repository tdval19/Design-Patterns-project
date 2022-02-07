from dataclasses import dataclass

from app.core.models.user import NO_ID

wallet_id: int = NO_ID


@dataclass
class Transaction:
    from_address: int
    to_address: int
    amount: float
    fee: float = 0
    transaction_id: int = NO_ID
