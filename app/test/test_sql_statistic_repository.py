# import random
# from pathlib import Path
# from typing import Tuple
#
# import pytest
#
# from app.infra.db.init_db import SqliteDbInitializer
# from app.infra.db.rep.statistic_repository import SqlStatisticRepository
# from app.test.db_path_fixture import get_db_script_path
#
#
# @pytest.fixture
# def repository(get_db_script_path: Path) -> SqlStatisticRepository:
#     db = SqliteDbInitializer(get_db_script_path, ":memory:")
#     return SqlStatisticRepository(db.get_connection())
#
#
# @pytest.fixture
# def example_update() -> Tuple[int, float]:
#     return 1, 5
#
#
# class TestSqlStatisticRepository:
#     def test_should_return_zeroes(self, repository: SqlStatisticRepository) -> None:
#         stats = repository.get()
#         assert stats.total_profit == 0.0
#         assert stats.num_of_transactions == 0
#
#     def test_should_update_values(
#         self, repository: SqlStatisticRepository, example_update: Tuple[int, float]
#     ) -> None:
#         before_stats = repository.get()
#         delta_transactions, delta_profit = example_update
#         repository.update(delta_transactions, delta_profit)
#         after_stats = repository.get()
#         assert (
#             after_stats.num_of_transactions - before_stats.num_of_transactions
#             == delta_transactions
#         )
#         assert after_stats.total_profit - before_stats.total_profit == delta_profit
#
#     def test_should_update_values_with_random(
#         self, repository: SqlStatisticRepository
#     ) -> None:
#         for i in range(20):
#             before_stats = repository.get()
#             delta_profit = round(random.random(), 3)
#             delta_transactions = 1
#             repository.update(delta_transactions, delta_profit)
#             after_stats = repository.get()
#             assert (
#                 after_stats.num_of_transactions - before_stats.num_of_transactions
#                 == delta_transactions
#             )
#             assert (
#                 after_stats.total_profit - before_stats.total_profit
#                 == pytest.approx(delta_profit)
#             )
