DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
  user_id INT PRIMARY KEY,
  email TEXT,
  password TEXT
);
DROP TABLE IF EXISTS user_modo;
CREATE TABLE IF NOT EXISTS user_modo (
  user_id INT PRIMARY KEY REFERENCES users(user_id),
  modo_account_id TEXT,
  modo_vault_id TEXT,
  last_four_credit_card TEXT
);
DROP TABLE IF EXISTS services;
CREATE TABLE IF NOT EXISTS services (
  service_id INT PRIMARY KEY,
  name TEXT,
  cost TEXT
);
DROP TABLE IF EXISTS user_subscriptions;
CREATE TABLE IF NOT EXISTS user_subscriptions (
  subscription_id INT PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  service_id INT REFERENCES services(service_id),
  username TEXT,
  password TEXT,
  is_active BOOLEAN,
  activity_ts TIMESTAMP,
  next_charge_dt DATE,
  next_charge_amt DOUBLE PRECISION
);
DROP TABLE IF EXISTS transaction_history;
CREATE TABLE IF NOT EXISTS transaction_history (
  transaction_id INT PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  service_id INT REFERENCES services(service_id),
  transaction_ts TIMESTAMP,
  transaction_amt DOUBLE PRECISION
);

INSERT INTO users VALUES (1, 'kperry@yomail.com', 'tswifty');
INSERT INTO services VALUES (1, 'Spotify', '9.99');
INSERT INTO services VALUES (2, 'Netflix', '9.99');
INSERT INTO services VALUES (3, 'LastPass', '12.00');
INSERT INTO services VALUES (4, 'BirchBox', '10.00');
INSERT INTO user_modo VALUES (1, '71033440-6aa3-46f3-accb-30a6387bdd67', '176a2c58-ee13-4d97-b3cf-45b6d3bf1a76', '5432');
INSERT INTO user_subscriptions VALUES (1, 1, 1, 'ktperryfan007', 'tswifty', 0, '2016-10-22', NULL, 9.99);
INSERT INTO user_subscriptions VALUES (2, 1, 2, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO user_subscriptions VALUES (3, 1, 3, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO user_subscriptions VALUES (4, 1, 4, NULL, NULL, 0, NULL, NULL, NULL);
