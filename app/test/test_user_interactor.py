import sqlite3
from pathlib import Path
from sqlite3 import Connection

import pytest
from app.core.interactors.users import UserInteractor
from app.core.interactors.users import UserNotFoundException
from app.core.models.user import User
from app.infra.db.init_db import SqliteDbInitializer
from app.infra.db.rep.user_repository import SqlUserRepository


@pytest.fixture
def connection(get_db_script_path: Path) -> sqlite3.Connection:
    db = SqliteDbInitializer(get_db_script_path, ":memory:")
    connection = db.get_connection()
    return connection


class TestUserInteractor:
    def test_add_user(self, connection: Connection) -> None:
        user_repository = SqlUserRepository(connection)
        user_interactor = UserInteractor(user_repository)
        new_user = user_interactor.create_user()
        get_user = user_repository.get_by_id(new_user.user_id)
        assert new_user == get_user

    def test_get_user(self, connection: Connection) -> None:
        user_repository = SqlUserRepository(connection)
        user_interactor = UserInteractor(user_repository)
        new_user = user_repository.add(User())
        assert new_user == user_interactor.get_user(new_user.user_id)

    def test_get_user_none(self, connection: Connection) -> None:
        user_repository = SqlUserRepository(connection)
        user_interactor = UserInteractor(user_repository)

        with pytest.raises(UserNotFoundException):
            user_interactor.get_user(-1)

        none_user_repo = user_repository.get_by_id(-1)
        assert none_user_repo is None
