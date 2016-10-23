"""Subscribely's Modo actions with database integration."""

import json
import sqlite3

import subscribely.modo_api as modo_api

def register_user(connection, user_id, phone_number, first_name=None, last_name=None, email=None):
    cursor = connection.cursor()
    response = modo_api.register_user(phone_number, first_name, last_name, email)

    print(response.text)
    if response.status_code != 200:
        raise Exception('Response status code <{}>'.format(response.status_code))
    else:
        response_data = json.loads(response.text)['response_data']
        cursor.execute('INSERT INTO user_modo VALUES (?, ?, ?, ?)', (user_id, response_data['account_id'], None, None))
        connection.commit()

def add_credit_card(connection, user_id, name_on_card, credit_card_number, expiration_month,
    expiration_year, security_code, billing_address, zip_code):

    cursor = connection.cursor()
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

def process_payment_virtual_cc(connection, user_id, service_id):
    """Charges payment on user for service. Returns virtual credit card detail."""
    cursor = connection.cursor()
    modo_account_id = cursor.execute('SELECT modo_account_id FROM user_modo WHERE user_id = ?;', (user_id,)).fetchone()[0]
    amount = cursor.execute('SELECT next_charge_amt FROM user_subscriptions WHERE user_id = ? AND service_id = ?;', (user_id, service_id)).fetchone()[0]
    vault_id = cursor.execute('SELECT modo_vault_id FROM user_modo WHERE user_id = ?;', (user_id,)).fetchone()[0] 

    mint_response = modo_api.mint_coin_cc(modo_account_id, amount, vault_id)
    if mint_response.status_code != 200:
        raise Exception('Response status code <{}>'.format(response.status_code))
    print(mint_response.text)
    coin_id = json.loads(mint_response.text)['response_data']['coin_id']

    operate_response = modo_api.operate_coin(coin_id)
    if operate_response.status_code != 200:
        raise Exception('Response status code <{}>'.format(response.status_code))
    print(operate_response.text)
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

def process_payment_virtual_gc(connection, user_id, service_id):
    cursor = connection.cursor()
    modo_account_id = cursor.execute('SELECT modo_account_id FROM user_modo WHERE user_id = ?;', (user_id,)).fetchone()[0]
    amount = cursor.execute('SELECT next_charge_amt FROM user_subscriptions WHERE user_id = ? AND service_id = ?;', (user_id, service_id)).fetchone()[0]
    vault_id = cursor.execute('SELECT modo_vault_id FROM user_modo WHERE user_id = ?;', (user_id,)).fetchone()[0] 
    service_name = cursor.execute('SELECT name FROM services WHERE service_id = ?;', (service_id,)).fetchone()[0]

    mint_response = modo_api.mint_coin_gc(modo_account_id, amount, vault_id, service_name)
    if mint_response.status_code != 200:
        raise Exception('Response status code <{}>'.format(response.status_code))
    print(mint_response.text)
    coin_id = json.loads(mint_response.text)['response_data']['coin_id']

    operate_response = modo_api.operate_coin(coin_id)
    if operate_response.status_code != 200:
        raise Exception('Response status code <{}>'.format(response.status_code))
    print(operate_response.text)

    instruments = json.loads(operate_response.text)['response_data']['instruments']
    for instrument in instruments.keys():
        if instruments[instrument].get('new_vault_item'):
            return {
                'pan': instruments[instrument]['new_vault_item']['encrypted']['pan'],
            }
    else:
        raise Exception('No new vault item was found.')

