"""A simple wrapper for the Modo API."""

import json
import jwt
import math
import os
import requests
import time

def make_header():
    token = jwt.encode({
            'api_key': os.environ['MODO_API_KEY'],
            'iat': math.floor(time.time())
        },
        os.environ['MODO_API_SECRET_KEY'],
        algorithm='HS256')
    headers = {'Authorization': 'Token ' + token.decode('utf-8'),
            'Content-Type': 'application/json',
            'Accept': 'application/json'}
    return headers

def register_user(phone_number, first_name=None, last_name=None, email=None):
    payload = json.dumps({
        'phone': int(phone_number),
        'fname': first_name,
        'lname': last_name,
        'email': email,
    })
    response = requests.post('https://hack.modoapi.com/1.0.0-dev/people/register',
            headers=make_header(), data=payload)
    return response

def get_user_profile(account_id):
    payload = json.dumps({'account_id': account_id}) 
    response = requests.post('https://hack.modoapi.com/1.0.0-dev/people/profile',
        headers=make_header(), data=payload)
    return response

def delete_user(account_id):
    payload = json.dumps({'account_id': account_id})
    response = requests.post('https://hack.modoapi.com/1.0.0-dev/people/delete',
        headers=make_header(), data=payload)
    return response

def add_credit_card(modo_account_id, name_on_card, credit_card_number,
        expiration_month, expiration_year, security_code, billing_address,
        zip_code):
    encrypted_data = {
        'pan': credit_card_number,
        'exp_month': expiration_month,
        'exp_year': expiration_year,
        'name': name_on_card,
        'address': billing_address,
        'zip': zip_code,
    }
    payload = json.dumps({
        'items': [{
            'vault_type': 'OPEN_CARD',
            'encrypted_data': encrypted_data,
            'account_id': modo_account_id
        }]
    })
    response = requests.post('https://hack.modoapi.com/1.0.0-dev/vault/add',
        headers=make_header(), data=payload)
    return response

def mint_coin_cc(account_id, amount, vault_id):
    """Mint a coin with OPEN_CARD->OPEN_CARD."""
    payload = json.dumps({
        'account_id': account_id,
        'amount': amount,
        'description': 'Subscribely minting coin OPEN_CARD->OPEN_CARD.',
        'inputs': [{
            'instrument_id': vault_id,
            'max_amount': amount
        }],
        'outputs': [{
            'instrument_id': vault_id, # TODO: Remove?
            'instrument_type': 'OPEN_CARD',
            'max_amount': amount
        }],
    })
    response = requests.post('https://hack.modoapi.com/1.0.0-dev/coin/mint',
        headers=make_header(), data=payload)
    return response

def mint_coin_gc(account_id, amount, vault_id, service_name):
    """Mint a coin with OPEN_CARD->GENERATED_GIFT_CARD."""
    # Get merchant_id
    response = requests.post('https://hack.modoapi.com/1.0.0-dev/merchant/list',
        headers=make_header())
    merchant_response = json.loads(response.text)['response_data']
    for merchant in merchant_response:
        if merchant['merchant_name'] == service_name:
            merchant_id = merchant['merchant_id']
            break
    else:
        raise Exception('Merchant not found.')

    # Mint
    payload = json.dumps({
        'account_id': account_id,
        'amount': amount,
        'description': 'Subscribely minting coin OPEN_CARD->GENERATED_GIFT_CARD.',
        'inputs': [{
            'instrument_id': vault_id,
            'max_amount': amount
        }],
        'outputs': [{
            'instrument_type': 'GENERATED_GIFT_CARD',
            'qualifier': merchant_id,
            'max_amount': amount
        }],
    })
    response = requests.post('https://hack.modoapi.com/1.0.0-dev/coin/mint',
        headers=make_header(), data=payload)
    return response

def operate_coin(coin_id):
    payload = json.dumps({
        'coin_id': coin_id,
        'reason': 'Subscribely transmitting payment.'
    })
    response = requests.post('https://hack.modoapi.com/1.0.0-dev/coin/operate',
        headers=make_header(), data=payload)
    return response

