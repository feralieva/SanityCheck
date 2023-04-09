import pytest
import requests
from codemonsters_api_checks.config import config

# Make a request to the payment endpoint with valid data
def test_valid_payment():
    url = f"{config['endpoint']}/payment_transactions"
    headers = {'Authorization': 'Basic 7D2BAF1CF37B13E2069D6956105BD0E739499BDB'}
    data = {
        'amount': '10.00',
        'currency': 'USD',
        'card_number': '4111111111111111',
        'card_holder': 'John Doe',
        'exp_date': '1223',
        'cvv': '123',
        'unique_id': '0e08644635ccb520c2eeb54f33865660'
    }
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 200
    assert response.json()['status'] == 'approved'
    
# Make a request to the payment endpoint with invalid authentication
def test_invalid_auth_payment():
    url = f"{config['endpoint']}/payment_transactions"
    headers = {'Authorization': 'Basic abcdefg1234567890'}
    data = {
        'amount': '10.00',
        'currency': 'USD',
        'card_number': '4111111111111111',
        'card_holder': 'John Doe',
        'exp_date': '1223',
        'cvv': '123',
        'unique_id': '0e08644635ccb520c2eeb54f33865668'
    }
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 401
    
# Make a request to the void endpoint with a non-existent payment ID
def test_nonexistent_void():
    url = f"{config['endpoint']}/payment_transactions"
    headers = {'Authorization': 'Basic 7D2BAF1CF37B13E2069D6956105BD0E739499BDB'}
    data = {'reference_id': '0e08644635ccb520c2eeb54f33865660'}
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 422
    assert response.json()['message'] == 'Payment not found'
    
# Make a request to the void endpoint with an existing void ID
def test_existing_void():
    url = f"{config['endpoint']}/payment_transactions"
    headers = {'Authorization': 'Basic 7D2BAF1CF37B13E2069D6956105BD0E739499BDB'}
    data = {'reference_id': '0e08644635ccb520c2eeb54f33865660'}
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'Payment already voided'

# Make a request to the void endpoint for nonexisting payment
def test_nonexisting_payment_void():
    url = f"{config['endpoint']}/payment_transactions"
    headers = {'Authorization': 'Basic 7D2BAF1CF37B13E2069D6956105BD0E739499BDB'}
    data = {'reference_id': '0e08644635ccb520c2eeb54f33865668'}
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 422
    assert response.json()['message'] == 'Payment doesn\'t exist'