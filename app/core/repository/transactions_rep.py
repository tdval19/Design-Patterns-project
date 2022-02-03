import sqlite3
from typing import Protocol, List
from app.core.models import transaction


class ITransactionRepository(Protocol):

    def get_user_transactions(self, user_id: int) -> List[transaction.Transaction]:
        pass

    def get_wallet_transactions(self, user_id: int, wallet_address: int) -> List[transaction.Transaction]:
        pass

    def make_transfer(self) -> bool:
        pass


class TransactionRepository(ITransactionRepository):

    def __init__(self):
        self.connection = sqlite3.connect('project_db')
        self.cursor = self.connection.cursor()

    def get_user_transactions(self, user_id: int) -> List[transaction.Transaction]:
        pass

    def get_wallet_transactions(self,  user_id: int, wallet_address: int) -> List[transaction.Transaction]:
        pass

    def make_transfer(self) -> bool:
        pass
