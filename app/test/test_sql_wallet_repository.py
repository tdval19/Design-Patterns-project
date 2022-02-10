from app.core.models.wallet import Wallet
from app.infra.db.rep.user_repository import SqlUserRepository

rep = SqlUserRepository("test.db")


def test_should_return_none() -> None:
    assert rep.get_by_id(-1) is None


