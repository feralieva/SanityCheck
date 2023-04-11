import pytest
import requests
from codemonsters_api_checks.config import config

URL_TRANSACTIONS = f"{config['endpoint']}/payment_transactions"
UNIQUE_ID = ""

def get_basic_authentication():
    username = f"{config['username']}"
    password = f"{config['password']}"
    return {'Authorization': 'Basic ' + f'{username}:{password}'}

# Make a request to the payment endpoint with valid data
def test_valid_payment():
    headers = get_basic_authentication()
    data = {
        'amount': '10.00',
        'currency': 'USD',
        'card_number': '4111111111111111',
        'card_holder': 'John Doe',
        'exp_date': '1223',
        'cvv': '123',
    }
    response = requests.post(URL_TRANSACTIONS, headers=headers, json=data)
    assert response.status_code == 200
    assert response.json()['status'] == 'approved'
    assert 'unique_id' in response.json
    UNIQUE_ID = response.json()['unique_id']
    
# Make a request to the payment endpoint with invalid authentication
def test_invalid_auth_payment():
    username = f"{config['username']}"
    password = "wrong_password"
    headers = {'Authorization': 'Basic ' + f'{username}:{password}'}
    data = {
        'amount': '10.00',
        'currency': 'USD',
        'card_number': '4111111111111111',
        'card_holder': 'John Doe',
        'exp_date': '1223',
        'cvv': '123',
    }
    response = requests.post(URL_TRANSACTIONS, headers=headers, json=data)
    assert response.status_code == 401
    
# Make a request to the void endpoint with a non-existent payment ID
def test_nonexistent_void():
    headers = get_basic_authentication()
    data = {'reference_id': '0e08644635ccb520c2eeb54f33865660'}
    response = requests.post(URL_TRANSACTIONS, headers=headers, json=data)
    assert response.status_code == 422
    assert response.json()['message'] == 'Payment not found'
    
# Make a request to the void endpoint with an existing void ID
def test_existing_void():
    headers = get_basic_authentication()
    data = {'reference_id': UNIQUE_ID}
    response = requests.post(URL_TRANSACTIONS, headers=headers, json=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'Payment already voided'

# Make a request to the void endpoint for nonexisting payment
def test_nonexisting_payment_void():
    headers = get_basic_authentication()
    data = {'reference_id': '0e08644635ccb520c2eeb54f33865668'}
    response = requests.post(URL_TRANSACTIONS, headers=headers, json=data)
    assert response.status_code == 422
    assert response.json()['message'] == 'Payment doesn\'t exist'