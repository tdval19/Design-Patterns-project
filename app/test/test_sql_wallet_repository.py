from app.core.models.wallet import Wallet
from app.infra.db.rep.wallet_repository import SqlWalletRepository

rep = SqlWalletRepository("test.db")


def test_add_get_by_address() -> None:
    wallet = Wallet(1, 5.12, 2)
    rep.add(wallet)
    get_wallet = rep.get_by_address(2)
    assert wallet == get_wallet
    wallet = Wallet(5, 136.7, 3)
    rep.add(wallet)
    get_wallet = rep.get_by_address(3)
    assert wallet == get_wallet


def test_update_balance() -> None:
    wallet = Wallet(5, 100, 10)
    rep.add(wallet)
    get_wallet = rep.get_by_address(10)
    assert wallet == get_wallet
    rep.update_wallet_balance(10, 200)
    expected_wallet = Wallet(5, 200, 10)
    assert rep.get_by_address(10) == expected_wallet
