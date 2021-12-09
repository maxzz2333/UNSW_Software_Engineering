import requests
from src import config
from src.helpers import generate_jwt
'''
InputError when any of:
      
        channel_id does not refer to a valid channel
        u_id does not refer to a valid user
        u_id refers to a user who is not a member of the channel
        u_id refers to a user who is already an owner of the channel

AccessError when:
      
        channel_id is valid and the authorised user does not have owner permissions in the channel
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

def test_channel_addowner_channel_owner():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    auth_response3 = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    assert auth_response3.status_code == SUCCESS_CODE
    user3_token = auth_response3.json()['token']
    user3_id = auth_response3.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user2_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user3_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user2_token, 'channel_id': channel_data, 'u_id': user3_id})
    assert addowner_response.status_code == SUCCESS_CODE

def test_channel_addowner_global_owner():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    auth_response3 = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    assert auth_response3.status_code == SUCCESS_CODE
    user3_token = auth_response3.json()['token']
    user3_id = auth_response3.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user2_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user1_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    join_response2 = requests.post(f"{config.url}channel/join/v2",json={'token': user3_token, 'channel_id': channel_data})
    assert join_response2.status_code == SUCCESS_CODE

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user3_id})
    assert addowner_response.status_code == SUCCESS_CODE

def test_channel_addowner_channel_not_owner():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    auth_response3 = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    assert auth_response3.status_code == SUCCESS_CODE
    user3_token = auth_response3.json()['token']
    user3_id = auth_response3.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    join_response2 = requests.post(f"{config.url}channel/join/v2",json={'token': user3_token, 'channel_id': channel_data})
    assert join_response2.status_code == SUCCESS_CODE

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user2_token, 'channel_id': channel_data, 'u_id': user3_id})
    assert addowner_response.status_code == ACCESS_ERROR_CODE

def test_channel_addowner_invalid_channel_id():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user2_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user1_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user2_token, 'channel_id': 'a', 'u_id': user1_id})
    assert addowner_response.status_code == INPUT_ERROR_CODE

def test_channel_addowner_invalid_u_id():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user1_token, 'channel_id': channel_data, 'u_id': -1})
    assert addowner_response.status_code == INPUT_ERROR_CODE

def test_channel_addowner_invalid_token(): 

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

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': -1, 'channel_id': channel_data, 'u_id': user2_id})
    assert addowner_response.status_code == ACCESS_ERROR_CODE

def test_channel_addowner_invalid_auth_user(): 

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

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': generate_jwt(user1_token, 2), 'channel_id': channel_data, 'u_id': user2_id})
    assert addowner_response.status_code == ACCESS_ERROR_CODE

def test_channel_addowner_authorised_user_is_not_a_member_of_the_channel(): 

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    auth_response3 = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    assert auth_response3.status_code == SUCCESS_CODE
    user3_id = auth_response3.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user2_token, 'channel_id': channel_data, 'u_id': user3_id})
    assert addowner_response.status_code == ACCESS_ERROR_CODE

def test_channel_addowner_u_id_not_a_member_of_the_channel():

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

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert addowner_response.status_code == INPUT_ERROR_CODE

def test_channel_addowner_u_id_already_a_global_owner():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user2_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user1_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user2_token, 'channel_id': channel_data, 'u_id': user1_id})
    assert addowner_response.status_code == SUCCESS_CODE

def test_channel_addowner_u_id_already_a_channel_owner():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    auth_response3 = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    assert auth_response3.status_code == SUCCESS_CODE
    user3_token = auth_response3.json()['token']
    user3_id = auth_response3.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user2_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user3_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user2_token, 'channel_id': channel_data, 'u_id': user3_id})
    assert addowner_response.status_code == SUCCESS_CODE

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user2_token, 'channel_id': channel_data, 'u_id': user3_id})
    assert addowner_response.status_code == INPUT_ERROR_CODE