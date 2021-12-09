import requests
from src import config
from src.helpers import generate_jwt

'''
InputError when any of:
      
        channel_id does not refer to a valid channel
        u_id does not refer to a valid user
        u_id refers to a user who is already a member of the channel
      
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

USER_3 = {'email': "z5362199@ad.unsw.edu.au",
         'password': "password", 
         'name_first': "Hao",
         'name_last': "Chen" }

USER_4 = {'email': "z5191599@ad.unsw.edu.au",
         'password': "password", 
         'name_first': "Zhang",
         'name_last': "Zhao" }

def test_channel_invite_valid():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_id = auth_response2.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert invite_response.status_code == SUCCESS_CODE

def test_channel_invite_invalid_channel_id_invalid_format():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_id = auth_response2.json()['auth_user_id']

    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user1_token, 'channel_id': 'a', 'u_id': user2_id})
    assert invite_response.status_code == INPUT_ERROR_CODE

def test_channel_invite_invalid_channel_id_invalid_value():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_id = auth_response2.json()['auth_user_id']

    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user1_token, 'channel_id': -1, 'u_id': user2_id})
    assert invite_response.status_code == INPUT_ERROR_CODE

def test_channel_invite_invalid_u_id_invalid_format():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user1_token, 'channel_id': channel_data, 'u_id': 'a'})
    assert invite_response.status_code == INPUT_ERROR_CODE

def test_channel_invite_invalid_u_id_invalid_value():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user1_token, 'channel_id': channel_data, 'u_id': -1})
    assert invite_response.status_code == INPUT_ERROR_CODE

def test_channel_invite_uid_already_in_channel_owner():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user1_id})
    assert invite_response.status_code == INPUT_ERROR_CODE

def test_channel_invite_uid_already_in_channel_member():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_id = auth_response2.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert invite_response.status_code == SUCCESS_CODE

    invite_response2 = requests.post(f"{config.url}channel/invite/v2",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert invite_response2.status_code == INPUT_ERROR_CODE

def test_channel_invite_uid_already_in_channel_complex():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']
    user2_id = auth_response2.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert invite_response.status_code == INPUT_ERROR_CODE

def test_channel_invite_authorised_user_is_not_a_member():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user2_token, 'channel_id': channel_data, 'u_id': user1_id})
    assert invite_response.status_code == ACCESS_ERROR_CODE
        
def test_channel_invite_authorised_user_exists_but_not_in_this_channel():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    auth_response3 = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    assert auth_response.status_code == SUCCESS_CODE
    user3_token = auth_response3.json()['token']
    user3_id = auth_response3.json()['auth_user_id']

    auth_response4 = requests.post(f"{config.url}auth/register/v2", json=USER_4)
    assert auth_response4.status_code == SUCCESS_CODE
    user4_id = auth_response4.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    channel_response2 = requests.post(f"{config.url}channels/create/v2",json={'token': user2_token, 'name': 'Test channel2', 'is_public': True})
    assert channel_response2.status_code == SUCCESS_CODE
    channel_data2 = channel_response2.json()['channel_id']

    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user3_id})
    assert invite_response.status_code == SUCCESS_CODE

    invite_response2 = requests.post(f"{config.url}channel/invite/v2",json={'token': user3_token, 'channel_id': channel_data2, 'u_id': user4_id})
    assert invite_response2.status_code == ACCESS_ERROR_CODE

def test_channel_invite_invalid_auth_user():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_id = auth_response2.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': generate_jwt(user1_token, 2), 'channel_id': channel_data, 'u_id': user2_id})
    assert invite_response.status_code == ACCESS_ERROR_CODE

def test_channel_invite_invalid_token():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_id = auth_response2.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': -1, 'channel_id': channel_data, 'u_id': user2_id})
    assert invite_response.status_code == ACCESS_ERROR_CODE