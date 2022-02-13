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
        pass

    def test_authorise_user(self, connection: sqlite3.Connection):
        user_repo = SqlUserRepository(connection)
        simple_auth = SimpleAuth(user_repo, SimpleKeyEncoder())
        pass

    def test_user_has_permission(self, connection: sqlite3.Connection):
        user_repo = SqlUserRepository(connection)
        simple_auth = SimpleAuth(user_repo, SimpleKeyEncoder())
        pass

    def test_authorise_admin(self, connection: sqlite3.Connection):
        user_repo = SqlUserRepository(connection)
        simple_auth = SimpleAuth(user_repo, SimpleKeyEncoder())
        pass
