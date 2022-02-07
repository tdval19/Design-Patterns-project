from dataclasses import dataclass


@dataclass
class Transaction:
    transaction_id: int
    from_address: int
    to_address: int
    amount: float
    fee: float = 0
