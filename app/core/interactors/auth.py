from dataclasses import dataclass, field
from typing import Protocol, Optional
from app.core.repository.repository_interfaces import IUserRepository


@dataclass
class UserCredentials:
    user_id: int


class IUserAuth(Protocol):
    def generate_key(self, credentials: UserCredentials) -> str:
        pass

    def authorize_user(self, key: Optional[str]) -> UserCredentials:
        pass

    def user_has_permission(
        self, key: Optional[str], user_id_has_permission: int
    ) -> None:
        pass

    def authorize_admin(self, key: Optional[str]) -> None:
        pass


@dataclass
class IKeyEncoder:
    def decode_key(self, key: str) -> UserCredentials:
        pass

    def encode_key(self, credentials: UserCredentials) -> str:
        pass


@dataclass
class SimpleAuth(IUserAuth):
    repository: IUserRepository
    encoder: IKeyEncoder
    admin_key = "ADMIN_KEY"

    def generate_key(self, credentials: UserCredentials) -> str:
        return self.encoder.encode_key(credentials)

    def authorize_user(self, key: Optional[str]) -> UserCredentials:
        credentials = None
        if key is None:
            raise NotAuthorizedException("authorization required")
        try:
            credentials = self.encoder.decode_key(key)
        except ValueError:
            raise NotAuthorizedException("invalid user key")

        if self.repository.get_by_id(credentials.user_id) is None:
            raise NotAuthorizedException("incorrect user key")
        return credentials

    def user_has_permission(
        self, key: Optional[str], user_id_has_permission: int
    ) -> None:
        credentials = None
        if key is None:
            raise NotAuthorizedException("authorization required")

        try:
            credentials = self.encoder.decode_key(key)
        except ValueError:
            raise NotAuthorizedException("invalid user key")

        if credentials.user_id != user_id_has_permission:
            raise ForbiddenException("you don't have permission to do this")

    def authorize_admin(self, key: Optional[str]) -> None:
        if key is None:
            raise NotAuthorizedException("authorization required")
        if self.admin_key != key:
            raise NotAuthorizedException("incorrect admin key")


class NotAuthorizedException(Exception):
    def __init__(self, message: str):
        self.message = message


class ForbiddenException(Exception):
    def __init__(self, message: str):
        self.message = message
