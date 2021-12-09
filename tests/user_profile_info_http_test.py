import requests
from src import config
from src.helpers import generate_jwt
from src.config import *

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

def test_profileinfo_invalid_token():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    user_response = requests.get(f"{config.url}user/profile/v1", params={'token': 'invalidtoken', 'u_id': 99})
    assert user_response.status_code == ACCESS_ERROR_CODE

def test_profileinfo_invalid_user():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    user_response = requests.get(f"{config.url}user/profile/v1", params={'token': generate_jwt(99), 'u_id': 99})
    assert user_response.status_code == ACCESS_ERROR_CODE

def test_profileinfo_nonexistent_user():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    user_response = requests.get(f"{config.url}user/profile/v1", params={'token': user1_token, 'u_id': 99})
    assert user_response.status_code == INPUT_ERROR_CODE
    

def test_profileinfo_self():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']

    user_response = requests.get(f"{config.url}user/profile/v1", params={'token': user1_token, 'u_id': user1_id})
    assert user_response.status_code == SUCCESS_CODE
    profile = user_response.json()

    assert profile == {
        'user': {
            'u_id': user1_id,
            'email': "z5362100@ad.unsw.edu.au", 
            'name_first': "Glenn",
            'name_last': "Deng",
            'handle_str': "glenndeng",
            'profile_img_url': url + 'static/default.jpg'
        }
    }
  

def test_profileinfo_diffuser():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response1.status_code == SUCCESS_CODE
    user1_id = auth_response1.json()['auth_user_id']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    user_response = requests.get(f"{config.url}user/profile/v1", params={'token': user2_token, 'u_id': user1_id})
    assert user_response.status_code == SUCCESS_CODE
    profile = user_response.json()

    assert profile == {
        'user': {
            'u_id': user1_id,
            'email': "z5362100@ad.unsw.edu.au", 
            'name_first': "Glenn",
            'name_last': "Deng",
            'handle_str': "glenndeng",
            'profile_img_url': url + 'static/default.jpg'
        }
    }

def test_profileinfo_removed_user():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response1.status_code == SUCCESS_CODE
    user1_token = auth_response1.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_id = auth_response2.json()['auth_user_id']

    remove_response = requests.delete(f"{config.url}admin/user/remove/v1",json={'token': user1_token, 'u_id': user2_id})
    assert remove_response.status_code == SUCCESS_CODE

    user_response = requests.get(f"{config.url}user/profile/v1", params={'token': user1_token, 'u_id': user2_id})
    assert user_response.status_code == SUCCESS_CODE
    profile = user_response.json()

    assert profile == {
        'user': {
            'u_id': user2_id,
            'email': "z5191576@ad.unsw.edu.au", 
            'name_first': "Removed",
            'name_last': "user",
            'handle_str': "harveymiao",
            'profile_img_url': url + 'static/default.jpg'
        }
    }