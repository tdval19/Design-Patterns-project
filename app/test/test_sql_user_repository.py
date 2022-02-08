from pathlib import Path

from app.core.models.user import User
from app.infra.db.init_db import SqliteDbInitializer
from app.infra.db.rep.user_repository import SqlUserRepository

path = Path(__file__).parent / "../infra/db/scheme.sql"
db = SqliteDbInitializer(path, ":memory:")
rep = SqlUserRepository(db.get_connection())


def test_should_return_none() -> None:
    assert rep.get_by_id(-1) is None


def test_add_get() -> None:
    tmp_user = rep.add(User())
    user = rep.get_by_id(tmp_user.user_id)
    assert user is not None
    assert user.user_id == tmp_user.user_id
