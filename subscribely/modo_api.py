"""A simple wrapper for the Modo API."""

import json
import jwt
import math
import os
import requests
import time

token = jwt.encode({
        'api_key': os.environ['MODO_API_KEY'],
        'iat': math.floor(time.time())
    },
    os.environ['MODO_API_SECRET_KEY'],
    algorithm='HS256')
headers = {'Authorization': 'Token ' + token.decode('utf-8'),
        'Content-Type': 'application/json'}
#        'Accept': 'application/json'}

def register_user(phone_number, first_name=None, last_name=None, email=None):
    payload = json.dumps({
        'phone': int(phone_number),
        'fname': first_name,
        'lname': last_name,
        'email': email,
    })
    response = requests.post('https://hack.modoapi.com/1.0.0-dev/people/register',
            headers=headers, data=payload)
    return response

def get_user_profile(account_id):
    payload = json.dumps({'account_id': account_id}) 
    response = requests.post('https://hack.modoapi.com/1.0.0-dev/people/profile',
            headers=headers, data=payload)
    return response

def delete_user(account_id):
    payload = json.dumps({'account_id': account_id})
    response = requests.post('https://hack.modoapi.com/1.0.0-dev/people/delete',
            headers=headers, data=payload)
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
            headers=headers, data=payload)
    return response

def mint_coin():
    raise NotImplementedError

def operate_coin():
    raise NotImplementedError
