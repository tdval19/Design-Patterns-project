CREATE TABLE IF NOT EXISTS user_table(
  user_id INTEGER PRIMARY KEY AUTOINCREMENT
);
CREATE TABLE IF NOT EXISTS wallet_table (
  wallet_address INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  balance_btc DOUBLE,
  FOREIGN KEY (user_id) REFERENCES user_table (user_id)
);
CREATE TABLE IF NOT EXISTS transaction_table (
  transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
  from_wallet_address INTEGER,
  to_wallet_address INTEGER,
  bitcoin_quantity DOUBLE,
  fee DOUBLE,
  FOREIGN KEY (from_wallet_address) REFERENCES wallet_table (wallet_address),
  FOREIGN KEY (to_wallet_address) REFERENCES wallet_table (wallet_address)
);
CREATE TABLE IF NOT EXISTS statistics_table (
  total_profit DOUBLE, total_transactions INTEGER
);
