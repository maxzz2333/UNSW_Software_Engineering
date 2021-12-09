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

def test_admin_user_permission_change_to_global_owner():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    
    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_id = auth_response2.json()['auth_user_id']

    permission_response = requests.post(f"{config.url}admin/userpermission/change/v1",json={'token': user1_token, 'u_id': user2_id, 'permission_id': 1})
    assert permission_response.status_code == SUCCESS_CODE

def test_admin_user_permission_change_to_user():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    
    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_id = auth_response2.json()['auth_user_id']

    permission_response = requests.post(f"{config.url}admin/userpermission/change/v1",json={'token': user1_token, 'u_id': user2_id, 'permission_id': 1})
    assert permission_response.status_code == SUCCESS_CODE

    permission_response2 = requests.post(f"{config.url}admin/userpermission/change/v1",json={'token': user1_token, 'u_id': user2_id, 'permission_id': 2})
    assert permission_response2.status_code == SUCCESS_CODE

def test_admin_user_permission_change_invalid_u_id():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    permission_response = requests.post(f"{config.url}admin/userpermission/change/v1",json={'token': user1_token, 'u_id': -1, 'permission_id': 1})
    assert permission_response.status_code == INPUT_ERROR_CODE

def test_admin_user_permission_change_invalid_permission_id():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    
    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_id = auth_response2.json()['auth_user_id']

    permission_response = requests.post(f"{config.url}admin/userpermission/change/v1",json={'token': user1_token, 'u_id': user2_id, 'permission_id': -1})
    assert permission_response.status_code == INPUT_ERROR_CODE

def test_admin_user_permission_change_auth_user_not_global_owner():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_id = auth_response.json()['auth_user_id']
    
    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    permission_response = requests.post(f"{config.url}admin/userpermission/change/v1",json={'token': user2_token, 'u_id': user1_id, 'permission_id': 2})
    assert permission_response.status_code == ACCESS_ERROR_CODE

def test_admin_user_permission_change_only_global_owner():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']

    permission_response = requests.post(f"{config.url}admin/userpermission/change/v1",json={'token': user1_token, 'u_id': user1_id, 'permission_id': 2})
    assert permission_response.status_code == INPUT_ERROR_CODE

def test_admin_user_permission_change_self_change():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    
    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']
    user2_id = auth_response2.json()['auth_user_id']

    permission_response = requests.post(f"{config.url}admin/userpermission/change/v1",json={'token': user1_token, 'u_id': user2_id, 'permission_id': 1})
    assert permission_response.status_code == SUCCESS_CODE

    permission_response2 = requests.post(f"{config.url}admin/userpermission/change/v1",json={'token': user2_token, 'u_id': user2_id, 'permission_id': 2})
    assert permission_response2.status_code == SUCCESS_CODE

def test_admin_user_permission_change_invalid_auth_user():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_id = auth_response.json()['auth_user_id']

    permission_response = requests.post(f"{config.url}admin/userpermission/change/v1",json={'token': -1, 'u_id': user1_id, 'permission_id': 2})
    assert permission_response.status_code == ACCESS_ERROR_CODE

def test_admin_user_permission_change_already_global_owner():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    
    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_id = auth_response2.json()['auth_user_id']

    permission_response = requests.post(f"{config.url}admin/userpermission/change/v1",json={'token': user1_token, 'u_id': user2_id, 'permission_id': 1})
    assert permission_response.status_code == SUCCESS_CODE

    permission_response2 = requests.post(f"{config.url}admin/userpermission/change/v1",json={'token': user1_token, 'u_id': user2_id, 'permission_id': 1})
    assert permission_response2.status_code == INPUT_ERROR_CODE

def test_admin_user_permission_change_already_user():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    
    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_id = auth_response2.json()['auth_user_id']

    permission_response = requests.post(f"{config.url}admin/userpermission/change/v1",json={'token': user1_token, 'u_id': user2_id, 'permission_id': 2})
    assert permission_response.status_code == INPUT_ERROR_CODE


def test_admin_user_permission_change_invalid_token():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    
    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_id = auth_response2.json()['auth_user_id']

    permission_response = requests.post(f"{config.url}admin/userpermission/change/v1",json={'token': generate_jwt(user1_token, 2), 'u_id': user2_id, 'permission_id': 1})
    assert permission_response.status_code == ACCESS_ERROR_CODE
