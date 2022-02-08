import random
from pathlib import Path

import pytest

from app.infra.db.init_db import SqliteDbInitializer
from app.infra.db.rep.statistic_repository import SqlStatisticRepository

path = Path(__file__).parent / "../infra/db/scheme.sql"
db = SqliteDbInitializer(path, ":memory:")
rep = SqlStatisticRepository(db.get_connection())


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
