import sqlite3
from dataclasses import dataclass
from pathlib import Path
from sqlite3 import Connection


@dataclass
class SqliteDbInitializer:
    def __init__(self, script_path: Path, db_path: str) -> None:
        with open(script_path, "r") as sql_file:
            sql_script = sql_file.read()

        self.con = sqlite3.connect(db_path)
        cursor = self.con.cursor()
        cursor.executescript(sql_script)
        self.con.commit()

    def get_connection(self) -> Connection:
        return self.con
