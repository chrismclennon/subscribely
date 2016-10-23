"""Subscribely's Modo actions with database integration."""

import json
import sqlite3

import subscribely.modo_api as modo_api

#connection = sqlite3.connect('subscribely.db')
#cursor = connection.cursor()

#def _set_connection(conn):
#    global connection, cursor
#    connection = conn
#    cursor = connection.cursor()

def register_user(user_id, phone_number, first_name=None, last_name=None, email=None):
    response = modo_api.register_user(phone_number, first_name, last_name, email)

#    print(response.text)
    if response.status_code != 200:
        raise Exception('Response status code <{}>'.format(response.status_code))
    else:
        response_data = json.loads(response.text)['response_data']
        cursor.execute('INSERT INTO user_modo VALUES (?, ?, ?, ?)', (user_id, response_data['account_id'], None, None))
        connection.commit()

def add_credit_card(connection, user_id, name_on_card, credit_card_number, expiration_month,
    expiration_year, security_code, billing_address, zip_code):

    cursor=connection.cursor()
    modo_account_id = cursor.execute('SELECT modo_account_id FROM user_modo WHERE user_id = ?;', (user_id,)).fetchone()[0]
    response = modo_api.add_credit_card(modo_account_id, name_on_card,
        credit_card_number, expiration_month, expiration_year, security_code,
        billing_address, zip_code)
    print(response.text)
    if response.status_code != 200:
        raise Exception('Response status code <{}>'.format(response.status_code))
    else:
        vault_id = json.loads(response.text)['response_data'][0]['vault_id']
        cursor.execute('UPDATE user_modo SET last_four_credit_card=? WHERE user_id=?', (credit_card_number[-4:], user_id))
        cursor.execute('UPDATE user_modo SET modo_vault_id=? WHERE user_id=?', (vault_id, user_id))
        connection.commit()

def process_payment_virtual_cc(user_id, service_id):
    """Charges payment on user for service. Returns virtual credit card detail."""
    modo_account_id = cursor.execute('SELECT modo_account_id FROM user_modo WHERE user_id = ?;', (user_id,)).fetchone()[0]
    amount = cursor.execute('SELECT next_charge_amt FROM user_subscriptions WHERE user_id = ? AND service_id = ?;', (user_id, service_id)).fetchone()[0]
    vault_id = cursor.execute('SELECT modo_vault_id FROM user_modo WHERE user_id = ?;', (user_id,)).fetchone()[0] 

#    print(mint_response.text)
    mint_response = modo_api.mint_coin(modo_account_id, amount, vault_id)
    if mint_response.status_code != 200:
        raise Exception('Response status code <{}>'.format(response.status_code))
    coin_id = json.loads(mint_response.text)['response_data']['coin_id']

    operate_response = modo_api.operate_coin(coin_id)
    if operate_response.status_code != 200:
        raise Exception('Response status code <{}>'.format(response.status_code))
#    print(operate_response.text)
    instruments = json.loads(operate_response.text)['response_data']['instruments']
    for instrument in instruments.keys():
        if instruments[instrument].get('new_vault_item'):
            return {
                'pan': instruments[instrument]['new_vault_item']['encrypted']['pan'],
                'cvv': instruments[instrument]['new_vault_item']['encrypted']['cvv'],
                'exp_month': instruments[instrument]['new_vault_item']['encrypted']['exp_month'],
                'exp_year': instruments[instrument]['new_vault_item']['encrypted']['exp_year'],
            }
    else:
        raise Exception('No new vault item was found.')


if __name__ == '__main__':
    register_user(1, '5123349734')
    add_credit_card(1, 'Katy Perry', '5415240007992183', 12, 2020, 123, '123 Lane', '78703')

