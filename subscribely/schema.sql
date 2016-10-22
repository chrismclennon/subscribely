CREATE TABLE IF NOT EXISTS users (
  user_id INT PRIMARY KEY,
  name TEXT
);
CREATE TABLE IF NOT EXISTS user_modo (
  user_id INT PRIMARY KEY REFERENCES users(user_id),
  modo_account_id TEXT,
  is_active BOOLEAN
);
CREATE TABLE IF NOT EXISTS services (
  service_id INT PRIMARY KEY,
  name TEXT
);
CREATE TABLE IF NOT EXISTS user_subscriptions (
  user_id INT REFERENCES users(user_id),
  service_id INT REFERENCES services(service_id),
  username TEXT,
  password TEXT,
  is_active BOOLEAN,
  activity_ts TIMESTAMP,
  next_charge_dt DATE,
  next_charge_amt DOUBLE PRECISION
);
CREATE TABLE IF NOT EXISTS transaction_history (
  transaction_id INT PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  service_id INT REFERENCES services(service_id),
  transaction_ts TIMESTAMP,
  transaction_amt DOUBLE PRECISION
);
