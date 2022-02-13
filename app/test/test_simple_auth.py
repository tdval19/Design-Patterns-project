from sqlite3 import Connection

from app.core.interactors.auth import SimpleAuth, IUserAuth, IKeyEncoder
from app.core.interactors.auth import NotAuthorizedException
from app.core.interactors.auth import ForbiddenException
from app.core.interactors.auth import UserCredentials
import pytest
from pathlib import Path

from app.core.repository.repository_interfaces import IUserRepository
from app.infra.encoder.dummy_encoder import SimpleKeyEncoder
from app.infra.db.init_db import SqliteDbInitializer
from app.core.models.user import User
from app.infra.db.rep.user_repository import SqlUserRepository


@pytest.fixture
def connection(get_db_script_path: Path) -> Connection:
    db = SqliteDbInitializer(get_db_script_path, ":memory:")
    return db.get_connection()


@pytest.fixture
def user_repository(connection: Connection) -> IUserRepository:
    return SqlUserRepository(connection)


@pytest.fixture
def encoder() -> IKeyEncoder:
    return SimpleKeyEncoder()


@pytest.fixture
def auth(user_repository: IUserRepository, encoder: IKeyEncoder) -> IUserAuth:
    return SimpleAuth(user_repository, encoder)


class TestSimpleAuth:
    def test_generate_key(self, auth: IUserAuth) -> None:
        credentials = UserCredentials(1)
        assert isinstance(auth.generate_key(credentials), str)

    def test_authorise_user(
        self, user_repository: IUserRepository, auth: IUserAuth
    ) -> None:
        with pytest.raises(NotAuthorizedException):
            auth.authorize_user(None)
        with pytest.raises(NotAuthorizedException):
            auth.authorize_user("KEY_TEST")
        credentials = UserCredentials(1)
        key = auth.generate_key(credentials)
        with pytest.raises(NotAuthorizedException):
            auth.authorize_user(key)
        user = user_repository.add(User())
        credentials = UserCredentials(user.user_id)
        key = auth.generate_key(credentials)
        assert auth.authorize_user(key) == credentials

    def test_user_has_permission(self, auth: IUserAuth) -> None:
        with pytest.raises(NotAuthorizedException):
            auth.user_has_permission(None, 5)

        with pytest.raises(NotAuthorizedException):
            auth.user_has_permission("SOME_USER_KEY", 6)

        with pytest.raises(ForbiddenException):
            auth.user_has_permission("KEY6", 7)

    def test_authorise_admin(
        self, user_repository: IUserRepository, auth: IUserAuth
    ) -> None:
        # test key is non
        with pytest.raises(NotAuthorizedException):
            auth.authorize_admin(None)
        # test not authorised
        with pytest.raises(NotAuthorizedException):
            auth.authorize_admin("NON_ADMIN_KEY")
