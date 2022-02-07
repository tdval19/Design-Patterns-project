from dataclasses import dataclass

NO_ID: int = -1


@dataclass
class Wallet:
    user_id: int
    balance_btc: float
    wallet_id: int = NO_ID

