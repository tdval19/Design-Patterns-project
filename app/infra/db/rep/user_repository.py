import sqlite3
from dataclasses import dataclass
from typing import Optional

from app.core.models.user import User


@dataclass
class SqlUserRepository:
    db_name: str

    def get_by_id(self, user_id: int) -> Optional[User]:
        con = sqlite3.connect(self.db_name)
        statement = "SELECT user_id FROM  user_table WHERE user_id = ?"
        cursor = con.cursor()
        cursor.execute(statement, (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        con.close()
        if len(rows) == 0:
            return None
        return User(rows[0][0])

    def add(self, user: User) -> User:
        con = sqlite3.connect(self.db_name)
        statement = "INSERT INTO user_table values (null)"
        cursor = con.cursor()
        cursor.execute(statement)
        statement = "SELECT last_insert_rowid()"
        cursor.execute(statement)
        rows = cursor.fetchall()
        con.commit()
        cursor.close()
        con.close()
        user.user_id = rows[0][0]
        return user
