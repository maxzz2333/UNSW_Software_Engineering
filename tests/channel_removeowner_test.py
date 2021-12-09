import requests
from src import config
from src.helpers import generate_jwt
'''
InputError when any of:
      
        channel_id does not refer to a valid channel
        u_id does not refer to a valid user
        u_id refers to a user who is not an owner of the channel
        u_id refers to a user who is currently the only owner of the channel
      
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

def test_channel_removeowner_simple():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    
    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']
    user2_id = auth_response2.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert addowner_response.status_code == SUCCESS_CODE

    removeowner_response = requests.post(f"{config.url}channel/removeowner/v1",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert removeowner_response.status_code == SUCCESS_CODE

def test_channel_removeowner_invalid_channal_id():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    
    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']
    user2_id = auth_response2.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert addowner_response.status_code == SUCCESS_CODE

    removeowner_response = requests.post(f"{config.url}channel/removeowner/v1",json={'token': user1_token, 'channel_id': 'a', 'u_id': user2_id})
    assert removeowner_response.status_code == INPUT_ERROR_CODE

def test_channel_removeowner_invalid_u_id():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    removeowner_response = requests.post(f"{config.url}channel/removeowner/v1",json={'token': user1_token, 'channel_id': channel_data, 'u_id': -1})
    assert removeowner_response.status_code == INPUT_ERROR_CODE

def test_channel_removeowner_u_id_not_owner():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    
    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']
    user2_id = auth_response2.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    removeowner_response = requests.post(f"{config.url}channel/removeowner/v1",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert removeowner_response.status_code == INPUT_ERROR_CODE

def test_channel_removeowner_u_id_not_member():

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

    removeowner_response = requests.post(f"{config.url}channel/removeowner/v1",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert removeowner_response.status_code == INPUT_ERROR_CODE

def test_channel_removeowner_remove_itself():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    
    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']
    user2_id = auth_response2.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert addowner_response.status_code == SUCCESS_CODE

    removeowner_response = requests.post(f"{config.url}channel/removeowner/v1",json={'token': user2_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert removeowner_response.status_code == SUCCESS_CODE

def test_channel_removeowner_remove_only_one():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    removeowner_response = requests.post(f"{config.url}channel/removeowner/v1",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user1_id})
    assert removeowner_response.status_code == INPUT_ERROR_CODE

def test_channel_removeowner_token_invalid():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    
    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']
    user2_id = auth_response2.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert addowner_response.status_code == SUCCESS_CODE

    removeowner_response = requests.post(f"{config.url}channel/removeowner/v1",json={'token': 'a', 'channel_id': channel_data, 'u_id': user2_id})
    assert removeowner_response.status_code == ACCESS_ERROR_CODE

def test_channel_removeowner_auth_user_invalid():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    
    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']
    user2_id = auth_response2.json()['auth_user_id']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    addowner_response = requests.post(f"{config.url}channel/addowner/v1",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert addowner_response.status_code == SUCCESS_CODE

    removeowner_response = requests.post(f"{config.url}channel/removeowner/v1",json={'token': generate_jwt(user1_token, 2), 'channel_id': channel_data, 'u_id': user2_id})
    assert removeowner_response.status_code == ACCESS_ERROR_CODE

def test_channel_removeowner_remove_auth_user_not_member():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    removeowner_response = requests.post(f"{config.url}channel/removeowner/v1",json={'token': user2_token, 'channel_id': channel_data, 'u_id': user1_id})
    assert removeowner_response.status_code == ACCESS_ERROR_CODE

def test_channel_removeowner_remove_auth_user_not_owner():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']    

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    removeowner_response = requests.post(f"{config.url}channel/removeowner/v1",json={'token': user2_token, 'channel_id': channel_data, 'u_id': user1_id})
    assert removeowner_response.status_code == ACCESS_ERROR_CODE

def test_channel_removeowner_remove_auth_user_not_owner2():

    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']   

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']
    user2_id = auth_response2.json()['auth_user_id'] 

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user2_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user1_token, 'channel_id': channel_data})
    assert join_response.status_code == SUCCESS_CODE

    removeowner_response = requests.post(f"{config.url}channel/removeowner/v1",json={'token': user1_token, 'channel_id': channel_data, 'u_id': user2_id})
    assert removeowner_response.status_code == INPUT_ERROR_CODE
