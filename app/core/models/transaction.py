from dataclasses import dataclass


@dataclass
class Transaction:
    from_id: int
    to_id: int
    amount: float
