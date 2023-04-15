import pytest
import requests
import base64
from codemonsters_api_checks.config import config

URL_TRANSACTIONS = f"{config['endpoint']}/payment_transactions"
UNIQUE_ID = ""

def get_basic_authentication():
    username = f"{config['username']}"
    password = f"{config['password']}"
    credentials = f"{username}:{password}"
    b64_credentials = base64.b64encode(credentials.encode('ascii')).decode('ascii')
    return {'Authorization': 'Basic ' + b64_credentials}

# Make a request to the payment endpoint with valid data
def test_valid_payment():
    global UNIQUE_ID
    headers = get_basic_authentication()
    data = {
        'payment_transaction': {
            'card_number': '4200000000000000',
            'cvv': '123',
            'expiration_date': '06/2019',
            'amount': '500',
            'usage': 'Coffeemaker',
            'transaction_type': 'sale',
            'card_holder': 'Panda Panda',
            'email': 'panda@example.com',
            'address': 'Panda Street, China'
        }
    }
    response = requests.post(URL_TRANSACTIONS, headers=headers, json=data)
    assert response.status_code == 200
    assert 'unique_id' in response.json()
    UNIQUE_ID = response.json()['unique_id']
    
# Make a request to the payment endpoint with invalid authentication
def test_invalid_auth_payment():
    username = f"{config['username']}"
    password = "wrong_password"
    headers = {'Authorization': 'Basic ' + f'{username}:{password}'}
    data = {
        'payment_transaction': {
            'card_number': '4200000000000000',
            'cvv': '123',
            'expiration_date': '06/2019',
            'amount': '500',
            'usage': 'Coffeemaker',
            'transaction_type': 'sale',
            'card_holder': 'Panda Panda',
            'email': 'panda@example.com',
            'address': 'Panda Street, China'
        }
    }
    response = requests.post(URL_TRANSACTIONS, headers=headers, json=data)
    assert response.status_code == 401
    
# Make a request to the void endpoint with a non-existent payment ID
def test_nonexistent_void():
    headers = get_basic_authentication()
    data = {'reference_id': '0e08644635ccb520c2eeb54f33865660'}
    response = requests.post(URL_TRANSACTIONS, headers=headers, json=data)
    assert response.status_code == 422
    
# Make a request to the void endpoint with an existing void ID
def test_existing_void():
    global UNIQUE_ID
    headers = get_basic_authentication()
    print("UNIQUE_ID",UNIQUE_ID)
    data = {
        'payment_transaction': {
            'reference_id': UNIQUE_ID,
            'transaction_type': 'void'
        }
    }
    response = requests.post(URL_TRANSACTIONS, headers=headers, json=data)
    assert response.status_code == 200

# Make a request to the void endpoint for nonexisting payment
def test_nonexisting_payment_void():
    headers = get_basic_authentication()
    data = {'reference_id': '0e08644635ccb520c2eeb54f33865668'}
    response = requests.post(URL_TRANSACTIONS, headers=headers, json=data)
    assert response.status_code == 422