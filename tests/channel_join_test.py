import requests
from src import config
from src.helpers import generate_jwt

'''
InputError when any of:
      
        channel_id does not refer to a valid channel
        the authorised user is already a member of the channel
      
      AccessError when:
      
        channel_id refers to a channel that is private and the authorised user is not already a channel member and is not a global owner
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

USER_3 = {'email': "z5362199@ad.unsw.edu.au",
         'password': "password", 
         'name_first': "Hao",
         'name_last': "Chen" }

def test_channel_join_invalid_channel_id1_invalid_format():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channel/join/v2",json={'token': user1_token, 'channel_id': 'a'})
    assert channel_response.status_code == INPUT_ERROR_CODE

def test_channel_join_invalid_channel_id_invalid_number():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channel/join/v2",json={'token': user1_token, 'channel_id': -1})
    assert channel_response.status_code == INPUT_ERROR_CODE
        
def test_channel_join_token_invalid_format():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    channel_response2 = requests.post(f"{config.url}channel/join/v2",json={'token': 'a', 'channel_id': channel_data})
    assert channel_response2.status_code == ACCESS_ERROR_CODE
        
def test_channel_join_token_invalid_number():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    channel_response2 = requests.post(f"{config.url}channel/join/v2",json={'token': -1, 'channel_id': channel_data})
    assert channel_response2.status_code == ACCESS_ERROR_CODE

def test_channel_join_already_in_channel_public_owner():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    channel_response2 = requests.post(f"{config.url}channel/join/v2",json={'token': user1_token, 'channel_id': channel_data})
    assert channel_response2.status_code == INPUT_ERROR_CODE

def test_channel_join_already_in_channel_public_member():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    channel_response2 = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_data})
    assert channel_response2.status_code == SUCCESS_CODE

    channel_response3 = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_data})
    assert channel_response3.status_code == INPUT_ERROR_CODE

def test_channel_join_already_in_channel_private_owner():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': False})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    channel_response2 = requests.post(f"{config.url}channel/join/v2",json={'token': user1_token, 'channel_id': channel_data})
    assert channel_response2.status_code == INPUT_ERROR_CODE


def test_channel_join_private_channel_not_owner_or_global_owner():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': False})
    assert channel_response.status_code == SUCCESS_CODE

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    channel_response2 = requests.post(f"{config.url}channels/create/v2",json={'token': user2_token, 'name': 'Test channel', 'is_public': False})
    assert channel_response2.status_code == SUCCESS_CODE
    channel_data2 = channel_response2.json()['channel_id']

    auth_response3 = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    assert auth_response3.status_code == SUCCESS_CODE
    user3_token = auth_response3.json()['token']

    channel_response2 = requests.post(f"{config.url}channel/join/v2",json={'token': user3_token, 'channel_id': channel_data2})
    assert channel_response2.status_code == ACCESS_ERROR_CODE

def test_channel_join_private_channel_global_owner():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user2_token, 'name': 'Test channel', 'is_public': False})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    channel_response2 = requests.post(f"{config.url}channel/join/v2",json={'token': user1_token, 'channel_id': channel_data})
    assert channel_response2.status_code == SUCCESS_CODE

def test_channel_join_invalid_token():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    channel_response2 = requests.post(f"{config.url}channel/join/v2",json={'token': generate_jwt(user1_token, 2), 'channel_id': channel_data})
    assert channel_response2.status_code == ACCESS_ERROR_CODE

