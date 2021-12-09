import requests
import time
from src import config
from src.helpers import generate_jwt
'''
InputError when any of:
      
        channel_id does not refer to a valid channel
        length is a negative integer
        an active standup is currently running in the channel
      
      AccessError when:
      
        channel_id is valid and the authorised user is not a member of the channel
'''

ACCESS_ERROR_CODE = 403
INPUT_ERROR_CODE = 400
SUCCESS_CODE = 200

USER_1 = {'email': "z5362100@ad.unsw.edu.au",
         'password': "password", 
         'name_first': "Glenn",
         'name_last': "Deng" }

USER_2 = {'email': "z5191576@ad.unsw.edu.au",
         'password': "password", 
         'name_first': "Harvey",
         'name_last': "Miao" }

def test_standup_start_invalid_channel_id():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': user1_token, 'channel_id': 'invalid', 'length': 5})
    assert start_response.status_code == INPUT_ERROR_CODE

def test_standup_start_invalid_negative_length():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': user1_token, 'channel_id': channel_data, 'length': -1})
    assert start_response.status_code == INPUT_ERROR_CODE

def test_standup_start_an_active_stand_up_is_running():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']
    
    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': user1_token, 'channel_id': channel_data, 'length': 5})
    assert start_response.status_code == SUCCESS_CODE

    start_response2 = requests.post(f"{config.url}standup/start/v1",json={'token': user1_token, 'channel_id': channel_data, 'length': 5})
    assert start_response2.status_code == INPUT_ERROR_CODE

def test_standup_start_success():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']
    
    channel_response2 = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel2', 'is_public': True})
    assert channel_response2.status_code == SUCCESS_CODE
    channel_data = channel_response2.json()['channel_id']

    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': user1_token, 'channel_id': channel_data, 'length': 3})
    assert start_response.status_code == SUCCESS_CODE

    send_response = requests.post(f"{config.url}standup/send/v1",json={'token': user1_token, 'channel_id': channel_data, 'message': 'abcd'})
    assert send_response.status_code == SUCCESS_CODE

    time.sleep(4)

    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': user1_token, 'channel_id': channel_data, 'length': 3})
    assert start_response.status_code == SUCCESS_CODE

def test_standup_start_auth_user_not_member():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': user2_token, 'channel_id': channel_data, 'length': 5})
    assert start_response.status_code == ACCESS_ERROR_CODE

def test_standup_start_invalid_auth_user_id():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': 'invalid_id', 'channel_id': channel_data, 'length': 5})
    assert start_response.status_code == ACCESS_ERROR_CODE

def test_standup_start_invalid_token():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': generate_jwt(user1_token, 2), 'channel_id': channel_data, 'length': 5})
    assert start_response.status_code == ACCESS_ERROR_CODE