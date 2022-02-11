from dataclasses import dataclass

from app.core.models.user import User
from app.core.repository.repository_interfaces import IUserRepository


@dataclass
class UserInteractor:
    repository: IUserRepository

    def create_user(self) -> User:
        return self.repository.add(User())

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise NoUserFoundException(user_id)
        return user


class NoUserFoundException(Exception):
    def __init__(self, user_id: int):
        msg = "User with id: {} doesn't exist".format(user_id)
        super().__init__(msg)
