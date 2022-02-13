from pathlib import Path

import pytest

from app.core.models.user import User
from app.infra.db.init_db import SqliteDbInitializer
from app.infra.db.rep.user_repository import SqlUserRepository


@pytest.fixture
def repository(get_db_script_path: Path) -> SqlUserRepository:
    db = SqliteDbInitializer(get_db_script_path, ":memory:")
    return SqlUserRepository(db.get_connection())


class TestSqlUserRepository:
    def test_should_return_none(self, repository: SqlUserRepository) -> None:
        assert repository.get_by_id(-1) is None
        assert repository.get_by_id(1) is None

    def test_should_return_user_with_id_one(
        self, repository: SqlUserRepository
    ) -> None:
        assert repository.add(User()).user_id == 1

    def test_should_get_added_user(self, repository: SqlUserRepository) -> None:
        tmp_user = repository.add(User())
        user = repository.get_by_id(tmp_user.user_id)
        assert user is not None
        assert user.user_id == tmp_user.user_id
