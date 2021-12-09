import requests
from src import config
from src.helpers import generate_jwt
from src.config import *

ACCESS_ERROR_CODE = 403
INPUT_ERROR_CODE = 400
SUCCESS_CODE = 200
USER_1 = {'email': "z5191576@ad.unsw.edu.au",
         'password': "Somepassword", 
         'name_first': "Harvey",
         'name_last': "Miao" }
USER_2 = {"email": "z1234567@ad.unsw.edu.au",
         "password": "Somepassword", 
         "name_first": "Hayden",
         "name_last": "Smith" }
USER_3 = {"email": "z7654321@ad.unsw.edu.au",
         "password": "Somepassword", 
         "name_first": "Removed",
         "name_last": "user" }

def test_usersall_invalid_token():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    users_response = requests.get(f"{config.url}users/all/v1", params={'token': 'invalidtoken'})
    assert users_response.status_code == ACCESS_ERROR_CODE

def test_usersall_invalid_user():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    users_response = requests.get(f"{config.url}users/all/v1", params={'token': generate_jwt(99)})
    assert users_response.status_code == ACCESS_ERROR_CODE

def test_usersall_one_user():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']

    users_response = requests.get(f"{config.url}users/all/v1", params= {'token': user1_token})
    assert users_response.status_code == SUCCESS_CODE
    user_list = users_response.json()

    assert user_list == {
        'users': 
            [
                {
                    'u_id': user1_id,
                    'email': "z5191576@ad.unsw.edu.au",
                    'name_first': "Harvey",
                    'name_last': "Miao",
                    'handle_str': 'harveymiao',
                    'profile_img_url': url + 'static/default.jpg'
                }
            ]
    }

def test_usersall_simple():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response.status_code == SUCCESS_CODE
    user2_id = auth_response.json()['auth_user_id']

    users_response = requests.get(f"{config.url}users/all/v1", params= {'token': user1_token})
    assert users_response.status_code == SUCCESS_CODE
    user_list = users_response.json()

    assert user_list == {
        'users': 
            [
                {
                    'u_id': user1_id,
                    'email': "z5191576@ad.unsw.edu.au",
                    'name_first': "Harvey",
                    'name_last': "Miao",
                    'handle_str': 'harveymiao',
                    'profile_img_url': url + 'static/default.jpg'
                },
                {
                    'u_id': user2_id,
                    "email": "z1234567@ad.unsw.edu.au",
                    "name_first": "Hayden",
                    "name_last": "Smith",
                    'handle_str': 'haydensmith',
                    'profile_img_url': url + 'static/default.jpg'
                }
            ]
    }

def test_usersall_with_removed_user():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response.status_code == SUCCESS_CODE
    user2_id = auth_response.json()['auth_user_id']

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    assert auth_response.status_code == SUCCESS_CODE
    user3 = auth_response.json()

    # Show all before remove
    users_response = requests.get(f"{config.url}users/all/v1", params= {'token': user1_token})
    assert users_response.status_code == SUCCESS_CODE
    user_list = users_response.json()

    assert user_list == {
        'users': 
            [
                {
                    'u_id': user1_id,
                    'email': "z5191576@ad.unsw.edu.au",
                    'name_first': "Harvey",
                    'name_last': "Miao",
                    'handle_str': 'harveymiao',
                    'profile_img_url': url + 'static/default.jpg'
                },
                {
                    'u_id': user2_id,
                    "email": "z1234567@ad.unsw.edu.au",
                    "name_first": "Hayden",
                    "name_last": "Smith",
                    'handle_str': 'haydensmith',
                    'profile_img_url': url + 'static/default.jpg'
                },
                {
                    'u_id': user3['auth_user_id'],
                    "email": USER_3["email"],
                    "name_first": USER_3["name_first"],
                    "name_last": USER_3["name_last"],
                    'handle_str': 'removeduser',
                    'profile_img_url': url + 'static/default.jpg'
                }
            ]
    }

    # Remove user 3
    remove_response = requests.delete(f"{config.url}admin/user/remove/v1",json={'token': user1_token, 'u_id': user3['auth_user_id']})
    assert remove_response.status_code == SUCCESS_CODE

    # Show all again
    users_response = requests.get(f"{config.url}users/all/v1", params= {'token': user1_token})
    assert users_response.status_code == SUCCESS_CODE
    user_list = users_response.json()

    assert user_list == {
        'users': 
            [
                {
                    'u_id': user1_id,
                    'email': "z5191576@ad.unsw.edu.au",
                    'name_first': "Harvey",
                    'name_last': "Miao",
                    'handle_str': 'harveymiao',
                    'profile_img_url': url + 'static/default.jpg'
                },
                {
                    'u_id': user2_id,
                    "email": "z1234567@ad.unsw.edu.au",
                    "name_first": "Hayden",
                    "name_last": "Smith",
                    'handle_str': 'haydensmith',
                    'profile_img_url': url + 'static/default.jpg'
                }
            ]
    }