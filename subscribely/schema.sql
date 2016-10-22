-- noinspection SqlNoDataSourceInspectionForFile

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  user_id INT PRIMARY KEY,
  email TEXT,
  password TEXT
);

DROP TABLE IF EXISTS user_billing;
CREATE TABLE user_billing (
  -- Currently assumes: 1 credit card per customer
  user_id INT REFERENCES users(user_id),
  name_on_card TEXT,
  credit_card_number TEXT,
  expiration_month INT,
  expiration_year INT,
  security_code INT,
  zip_code TEXT
);

DROP TABLE IF EXISTS services;
CREATE TABLE services (
  service_id INT PRIMARY KEY,
  name TEXT
);

DROP TABLE IF EXISTS user_subscriptions;
CREATE TABLE user_subscriptions (
  user_id INT REFERENCES users(user_id),
  service_id INT REFERENCES services(service_id),
  is_active BOOLEAN,
  activity_ts TIMESTAMP,
  next_charge_dt DATE,
  next_charge_amt DOUBLE PRECISION
);

INSERT INTO users (email, password) VALUES ('kperry@yomail.com', 'tswifty')
