from dataclasses import dataclass
from typing import Optional

from app.core.models.user import User
from app.core.repository.repository_interfaces import IUserRepository


@dataclass
class UserInteractor:
    repository: IUserRepository

    def create_user(self) -> User:
        return self.repository.add(User())

    def get_user(self, user_id: int) -> Optional[User]:
        return self.repository.get_by_id(user_id)
