CREATE TABLE IF NOT EXISTS users (
  user_id INT PRIMARY KEY,
  name TEXT
);
CREATE TABLE IF NOT EXISTS user_billing (
  -- Currently assumes: 1 credit card per customer
  user_id INT REFERENCES users(user_id),
  name_on_card TEXT,
  credit_card_number TEXT,
  expiration_month INT,
  expiration_year INT,
  security_code INT,
  zip_code TEXT
);
CREATE TABLE IF NOT EXISTS services (
  service_id INT PRIMARY KEY,
  name TEXT
);
CREATE TABLE IF NOT EXISTS user_subscriptions (
  user_id INT REFERENCES users(user_id),
  service_id INT REFERENCES services(service_id),
  is_active BOOLEAN,
  activity_ts TIMESTAMP,
  next_charge_dt DATE,
  next_charge_amt DOUBLE PRECISION
);
