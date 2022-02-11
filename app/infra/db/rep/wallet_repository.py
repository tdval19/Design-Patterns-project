import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection
from typing import Optional, List

from app.core.models.wallet import Wallet
from app.core.repository.repository_interfaces import IWalletRepository


@dataclass
class SqlWalletRepository(IWalletRepository):
    con: Connection

    def get_by_address(self, wallet_address: int) -> Optional[Wallet]:
        statement = "SELECT user_id, balance_btc, wallet_address FROM  wallet_table WHERE wallet_address = ?"
        cursor = self.con.cursor()
        cursor.execute(statement, (wallet_address,))
        rows = cursor.fetchall()
        self.con.commit()
        cursor.close()
        if len(rows) == 0:
            return None
        return Wallet(rows[0][0], rows[0][1], rows[0][2])

    def update_wallet_balance(self, wallet_address: int, balance_btc: float) -> None:
        statement = "UPDATE wallet_table SET balance_btc=(?) WHERE wallet_address=?;"
        cursor = self.con.cursor()
        cursor.execute(statement, (balance_btc, wallet_address))
        self.con.commit()
        cursor.close()

    def add(self, wallet: Wallet) -> Wallet:
        statement = "INSERT INTO wallet_table(user_id, balance_btc) VALUES (?, ?)"
        cursor = self.con.cursor()
        cursor.execute(
            statement, (wallet.user_id, wallet.balance_btc)
        )
        self.con.commit()
        statement = "SELECT last_insert_rowid()"
        cursor.execute(statement)
        rows = cursor.fetchall()
        self.con.commit()
        cursor.close()
        wallet_address = rows[0][0]
        print(wallet_address)
        return Wallet(wallet.user_id, wallet.balance_btc, wallet_address)

    def get_wallets_by_user_id(self, user_id: int) -> List[Wallet]:
        statement = "SELECT balance_btc, wallet_address FROM wallet_table where user_id = ?";
        cursor = self.con.cursor()
        cursor.execute(statement, (user_id,))
        wallets = cursor.fetchall()
        res_list: List[Wallet] = []
        for wallet in wallets:
            wallet = Wallet(user_id, wallet[0], wallet[1])
            res_list.append(wallet)

        return res_list
