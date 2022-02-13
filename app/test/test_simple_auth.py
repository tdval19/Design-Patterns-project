import sqlite3

from app.core.interactors.auth import SimpleAuth
from app.core.interactors.auth import NotAuthorizedException
from app.core.interactors.auth import ForbiddenException
from app.core.interactors.auth import UserCredentials
import pytest
from pathlib import Path
from app.infra.encoder.dummy_encoder import SimpleKeyEncoder
from app.test.db_path_fixture import get_db_script_path
from app.infra.db.init_db import SqliteDbInitializer
from app.core.models.user import User
from app.infra.db.rep.user_repository import SqlUserRepository


@pytest.fixture
def connection(get_db_script_path: Path) -> sqlite3.Connection:
    db = SqliteDbInitializer(get_db_script_path, ":memory:")
    return db.get_connection()


class TestSimpleAuth:
    def test_generate_key(self, connection: sqlite3.Connection):
        user_repo = SqlUserRepository(connection)
        simple_auth = SimpleAuth(user_repo, SimpleKeyEncoder())
        credentials = UserCredentials(1)
        assert isinstance(simple_auth.generate_key(credentials), str)

    def test_authorise_user(self, connection: sqlite3.Connection):
        user_repo = SqlUserRepository(connection)
        simple_auth = SimpleAuth(user_repo, SimpleKeyEncoder())
        with pytest.raises(NotAuthorizedException):
            simple_auth.authorize_user(None)
        with pytest.raises(NotAuthorizedException):
            simple_auth.authorize_user("KEY_TEST")
        credentials = UserCredentials(1)
        key = simple_auth.generate_key(credentials)
        with pytest.raises(NotAuthorizedException):
            simple_auth.authorize_user(key)
        user = user_repo.add(User())
        credentials = UserCredentials(user.user_id)
        key = simple_auth.generate_key(credentials)
        assert simple_auth.authorize_user(key) == credentials

    def test_user_has_permission(self, connection: sqlite3.Connection):
        user_repo = SqlUserRepository(connection)
        simple_auth = SimpleAuth(user_repo, SimpleKeyEncoder())

        with pytest.raises(NotAuthorizedException):
            simple_auth.user_has_permission(None, 5)

        with pytest.raises(NotAuthorizedException):
            simple_auth.user_has_permission("SOME_USER_KEY", 6)

        with pytest.raises(ForbiddenException):
            simple_auth.user_has_permission("KEY6", 7)

    def test_authorise_admin(self, connection: sqlite3.Connection):
        user_repo = SqlUserRepository(connection)
        simple_auth = SimpleAuth(user_repo, SimpleKeyEncoder())
        # test key is non
        with pytest.raises(NotAuthorizedException):
            simple_auth.authorize_admin(None)
        # test not authorised
        with pytest.raises(NotAuthorizedException):
            simple_auth.authorize_admin("NON_ADMIN_KEY")
