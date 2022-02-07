from app.core.models.user import User
from app.infra.db.rep.user_repository import SqlUserRepository

rep = SqlUserRepository("test.db")


def test_should_return_none() -> None:
    assert rep.get_by_id(-1) is None


def test_add_get() -> None:
    tmp_user = rep.add(User(-1))
    user = rep.get_by_id(tmp_user.user_id)
    assert user is not None
    assert user.user_id == tmp_user.user_id

