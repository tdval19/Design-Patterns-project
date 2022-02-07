from dataclasses import dataclass
from typing import List

from app.core.models.wallet import Wallet


@dataclass
class User:
    user_id: int = -1
