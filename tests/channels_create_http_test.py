import requests
from src import config

ACCESS_ERROR_CODE = 403
INPUT_ERROR_CODE = 400
SUCCESS_CODE = 200
USER_1 = {'email': "z5191576@ad.unsw.edu.au",
         'password': "password", 
         'name_first': "Harvey",
         'name_last': "Miao" }

def test_create_single_channel():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user1_token = auth_response.json()['token']
    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_data = channel_response.json()

    assert channel_response.status_code == SUCCESS_CODE
    assert channel_data['channel_id'] == 1

def test_create_multi_channels():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user1_token = auth_response.json()['token']
    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel 1', 'is_public': True})
    channel_1_data = channel_response.json()

    assert channel_response.status_code == SUCCESS_CODE
    assert channel_1_data['channel_id'] == 1

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel 2', 'is_public': False})
    channel_2_data = channel_response.json()

    assert channel_response.status_code == SUCCESS_CODE
    assert channel_2_data['channel_id'] == 2

def test_create_with_invalid_token():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    requests.post(f"{config.url}auth/register/v2", json=USER_1)
    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': "wrongtoken123", 'name': 'Test channel 1', 'is_public': True})
    
    assert channel_response.status_code == ACCESS_ERROR_CODE

def test_create_with_long_channel_name():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user1_token = auth_response.json()['token']
    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'abcdefghijklmnopqrstuvwxyz', 'is_public': True})
    
    assert channel_response.status_code == INPUT_ERROR_CODE

def test_create_with_empty_channel_name():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user1_token = auth_response.json()['token']
    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': '', 'is_public': True})
    
    assert channel_response.status_code == INPUT_ERROR_CODE