from dataclasses import dataclass


@dataclass
class Transaction:
    from_address: int
    to_address: int
    amount: float
    fee: float = 0
    transaction_id: int = -1
