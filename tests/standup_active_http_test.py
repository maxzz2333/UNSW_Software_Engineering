import requests
import time
from src import config
from src.helpers import generate_jwt
'''
InputError when:
      
        channel_id does not refer to a valid channel
      
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

def test_standup_active_invalid_channel_id():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    active_response = requests.get(f"{config.url}standup/active/v1",params={'token': user1_token, 'channel_id': '-1'})
    assert active_response.status_code == INPUT_ERROR_CODE

def test_standup_active_not_a_member_of_the_channel():

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

    active_response = requests.get(f"{config.url}standup/active/v1",params={'token': user2_token, 'channel_id': channel_data})
    assert active_response.status_code == ACCESS_ERROR_CODE

def test_standup_active_invalid_auth_user_id():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    active_response = requests.get(f"{config.url}standup/active/v1",params={'token': generate_jwt(user1_token, 2), 'channel_id': channel_data})
    assert active_response.status_code == ACCESS_ERROR_CODE
    
def test_standup_active_invalid_token():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    active_response = requests.get(f"{config.url}standup/active/v1",params={'token': -1, 'channel_id': channel_data})
    assert active_response.status_code == ACCESS_ERROR_CODE

def test_standup_active_active():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    
    channel_response2 = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel2', 'is_public': True})
    assert channel_response2.status_code == SUCCESS_CODE
    channel_data = channel_response2.json()['channel_id']

    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': user1_token, 'channel_id': channel_data, 'length': 5})
    assert start_response.status_code == SUCCESS_CODE

    active_response = requests.get(f"{config.url}standup/active/v1",params={'token': user1_token, 'channel_id': channel_data})
    assert active_response.status_code == SUCCESS_CODE

    assert active_response.json()['is_active'] == True

def test_standup_active_not_active():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    active_response = requests.get(f"{config.url}standup/active/v1",params={'token': user1_token, 'channel_id': channel_data})
    assert active_response.status_code == SUCCESS_CODE

    assert active_response.json()['is_active'] == False
    assert active_response.json()['time_finish'] == None

