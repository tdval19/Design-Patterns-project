from app.core.models.transaction import Transaction
from app.infra.db.rep.transaction_repository import SqlTransactionRepository

rep = SqlTransactionRepository("test.db")


def test_add_get_by_wallet_different_account():
    transaction = Transaction(1, 2, 1.00, 1.5, 1)
    rep.add(transaction)
    transaction_list_from = rep.get_transactions_by_wallet_address(1)
    transaction_list_to = rep.get_transactions_by_wallet_address(2)
    assert len(transaction_list_from) == len(transaction_list_to) == 1
    assert transaction_list_from[0] == transaction_list_to[0] == transaction


def test_add_get_by_wallet_same_account():
    transaction = Transaction(1, 1, 500, 2.00, 1)
    rep.add(transaction)
    transaction_list = rep.get_transactions_by_wallet_address(1)
    assert len(transaction_list) == 1
    assert transaction_list[0] == transaction


def test_add_get_by_wallet_multiple_transactions():
    transaction_one = Transaction(1, 2, 1.00, 1.5, 1)
    transaction_two = Transaction(1, 1, 500, 2.00, 2)
    transaction_three = Transaction(2, 1, 666, 5.00, 3)
    transaction_four = Transaction(4, 3, 10, 3.00, 4)
    rep.add(transaction_one)
    rep.add(transaction_two)
    rep.add(transaction_three)
    rep.add(transaction_four)
    transaction_list_one = rep.get_transactions_by_wallet_address(1)
    transaction_list_two = rep.get_transactions_by_wallet_address(2)
    transaction_list_three = rep.get_transactions_by_wallet_address(3)
    transaction_list_four = rep.get_transactions_by_wallet_address(4)
    assert len(transaction_list_one) == 3
    assert len(transaction_list_two) == 2
    assert len(transaction_list_three) == 1
    assert len(transaction_list_four) == 1
    assert transaction_list_one[0] == transaction_one
    assert transaction_list_one[1] == transaction_two
    assert transaction_list_one[2] == transaction_three
    assert transaction_list_two[0] == transaction_three
    assert transaction_list_two[1] == transaction_one
    assert transaction_list_three[0] == transaction_four
    assert transaction_list_four[0] == transaction_four


# Will be done after wallet implementation
# def test_add_get_by_user():
#     pass
