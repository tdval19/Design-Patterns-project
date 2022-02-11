from dataclasses import dataclass

NO_ADDRESS: int = -1


@dataclass
class Wallet:
    user_id: int
    balance_btc: float
    wallet_address: int = NO_ADDRESS
