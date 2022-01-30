from dataclasses import dataclass
from typing import Optional

from app.core.models.user import User


@dataclass
class UserInteractor:
    def create_user(self) -> Optional[User]:
        pass
