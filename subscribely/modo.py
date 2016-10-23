"""Subscribely's Modo actions with database integration."""

import json
import modo_api
from retrying import retry
import sqlite3

connection = sqlite3.connect('subscribely.db')
cursor = connection.cursor()

def _retry_if_keyerror(exception):
    return isinstance(exception, KeyError)

@retry(retry_on_exception=_retry_if_keyerror, stop_max_attempt_number=12)
def register_user(user_id, phone_number, first_name=None, last_name=None, email=None):
    response = modo_api.register_user(phone_number,
        first_name, last_name, email)
    if response.status_code != 200:
        raise Exception('Response status code <{}>'.format(response.status_code))
    else:
        response_data = json.loads(response.text)['response_data']
        cursor.execute('INSERT INTO user_modo VALUES (?, ?, ?)', (user_id, response_data['account_id'], None))
        connection.commit()

def add_credit_card(user_id, name_on_card, credit_card_number, expiration_month,
    expiration_year, security_code, billing_address,  zip_code):
    modo_account_id = cursor.execute('SELECT modo_account_id FROM user_modo WHERE user_id = ?;', (user_id,)).fetchone()[0]
    response = modo_api.add_credit_card(modo_account_id, name_on_card,
        credit_card_number, expiration_month, expiration_year, security_code,
        billing_address, zip_code)
    print(response.text)
    if response.status_code != 200:
        raise Exception('Response status code <{}>'.format(response.status_code))
    else:
        vault_id = json.loads(response.text)['response_data']['vault_id']
        cursor.execute('UPDATE user_modo SET last_four_credit_card=? WHERE user_id=?', (credit_card_number[-4:], user_id))
        cursor.execute('UPDATE user_modo SET modo_vault_id=? WHERE user_id=?', (vault_id, user_id))
        connection.commit()



