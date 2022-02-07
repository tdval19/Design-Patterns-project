from dataclasses import dataclass
from typing import Optional

from app.core.models.user import User
from app.core.repository.repository_interfaces import IUserRepository


@dataclass
class UserInteractor:
    repository: IUserRepository

    def create_user(self) -> Optional[User]:
        pass
