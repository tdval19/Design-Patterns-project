import sqlite3
from dataclasses import dataclass
from typing import Optional

from app.core.models.wallet import Wallet
from app.core.repository.repository_interfaces import IWalletRepository


@dataclass
class SqlWalletRepository(IWalletRepository):
    db_name: str

    def get_by_address(self, wallet_address: int) -> Optional[Wallet]:
        con = sqlite3.connect(self.db_name)
        statement = "SELECT wallet_address FROM  wallet_table WHERE wallet_address = ?"
        cursor = con.cursor()
        cursor.execute(statement, (wallet_address,))
        rows = cursor.fetchall()
        con.commit()
        cursor.close()
        con.close()
        if len(rows) == 0:
            return None
        return Wallet(rows[0][0])

    def update_wallet_balance(self, wallet_address: int,  balance_btc: float) -> None:
        con = sqlite3.connect(self.db_name)
        statement = "UPDATE wallet_table SET balance_btc=(?) WHERE wallet_address=?;"
        cursor = con.cursor()
        cursor.execute(statement, (balance_btc, wallet_address))
        con.commit()
        cursor.close()
        con.close()

    def add(self, wallet: Wallet) -> None:
        con = sqlite3.connect(self.db_name)
        statement = "INSERT INTO wallet_table(wallet_address, user_id, balance_btc) VALUES (?, ?, ?)"
        cursor = con.cursor()
        cursor.execute(statement, (wallet.wallet_id, wallet.user_id, wallet.balance_btc))
        con.commit()
        cursor.close()
        con.close()
