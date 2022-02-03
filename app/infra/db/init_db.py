import sqlite3


class InitDb:

    def __init__(self) -> None:
        self.connection = sqlite3.connect('project_db')
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        create_user_table = '''CREATE TABLE IF NOT EXISTS user_table(user_id INTEGER PRIMARY KEY AUTOINCREMENT)'''
        self.cursor.execute(create_user_table)

        create_wallet_table = '''CREATE TABLE IF NOT EXISTS wallet_table
                                    (wallet_address INTEGER PRIMARY KEY AUTOINCREMENT, user_id,
                                    FOREIGN KEY (user_id)  REFERENCES user_table (user_id))'''
        self.cursor.execute(create_wallet_table)

        create_transaction_table = ''' CREATE TABLE IF NOT EXISTS transaction_table
                                        (transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        from_wallet_address, to_wallet_address, bitcoin_quantity INTEGER,
                                        FOREIGN KEY (from_wallet_address) REFERENCES wallet_table (wallet_address),
                                        FOREIGN KEY (to_wallet_address) REFERENCES wallet_table (wallet_address))'''
        self.cursor.execute(create_transaction_table)

        create_statistics_table = '''CREATE TABLE IF NOT EXISTS statistics_table (variable TEXT, value DOUBLE)'''
        self.cursor.execute(create_statistics_table)
