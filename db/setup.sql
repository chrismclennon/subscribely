DROP SCHEMA subscribely CASCADE;
CREATE SCHEMA IF NOT EXISTS subscribely;
CREATE TABLE IF NOT EXISTS subscribely.users (
  user_id INT PRIMARY KEY,
  name TEXT
);
CREATE TABLE IF NOT EXISTS subscribely.user_billing (
  -- Currently assumes: 1 credit card per customer
  user_id INT REFERENCES subscribely.users(user_id),
  name_on_card TEXT,
  credit_card_number TEXT,
  expiration_month INT,
  expiration_year INT,
  security_code INT,
  zip_code TEXT
);
CREATE TABLE IF NOT EXISTS subscribely.subscriptions (
  subscription_id INT PRIMARY KEY,
  name TEXT
);
CREATE TABLE IF NOT EXISTS subscribely.user_subscriptions (
  user_id INT REFERENCES subscribely.users(user_id),
  subscription_id INT REFERENCES subscribely.subscriptions(subscription_id),
  is_active BOOLEAN,
  activity_ts TIMESTAMP,
  next_charge_dt DATE,
  next_charge_amt DOUBLE PRECISION
);
