from dataclasses import dataclass

NO_ID: int = -1


@dataclass
class User:
    user_id: int = NO_ID
