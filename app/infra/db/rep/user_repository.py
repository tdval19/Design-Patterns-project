import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection
from typing import Optional

from app.core.models.user import User


@dataclass
class SqlUserRepository:
    con: Connection

    def get_by_id(self, user_id: int) -> Optional[User]:
        statement = "SELECT user_id FROM  user_table WHERE user_id = ?"
        cursor = self.con.cursor()
        cursor.execute(statement, (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        if len(rows) == 0:
            return None
        return User(rows[0][0])

    def add(self, user: User) -> User:
        statement = "INSERT INTO user_table values (null)"
        cursor = self.con.cursor()
        cursor.execute(statement)
        statement = "SELECT last_insert_rowid()"
        cursor.execute(statement)
        rows = cursor.fetchall()
        self.con.commit()
        cursor.close()
        user.user_id = rows[0][0]
        return user
