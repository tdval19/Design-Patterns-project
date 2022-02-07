import sqlite3

with open("scheme.sql", "r") as sql_file:
    sql_script = sql_file.read()

db = sqlite3.connect("bitcoin_wallet.db")
cursor = db.cursor()
cursor.executescript(sql_script)
db.commit()
db.close()
