import random

import pytest

from app.infra.db.rep.statistic_repository import SqlStatisticRepository

rep = SqlStatisticRepository("test.db")


def test_should_update_values() -> None:
    before_stats = rep.get()
    delta_profit = 5
    delta_transactions = 1
    rep.update(delta_transactions, delta_profit)
    after_stats = rep.get()
    assert (
        after_stats.num_of_transactions - before_stats.num_of_transactions
        == delta_transactions
    )
    assert after_stats.total_profit - before_stats.total_profit == delta_profit


def test_should_update_values_with_random() -> None:
    for i in range(20):
        before_stats = rep.get()
        delta_profit = round(random.random(), 3)
        delta_transactions = 1
        rep.update(delta_transactions, delta_profit)
        after_stats = rep.get()
        assert (
            after_stats.num_of_transactions - before_stats.num_of_transactions
            == delta_transactions
        )
        assert after_stats.total_profit - before_stats.total_profit == pytest.approx(
            delta_profit
        )
