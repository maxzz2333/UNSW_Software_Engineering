import requests
from src import config
from src.helpers import generate_jwt

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

def test_sethandle_invalid_token():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    sethandle_response = requests.put(f"{config.url}user/profile/sethandle/v1", json={'token': 'invalidtoken', 'handle_str': "imsocool"})
    assert sethandle_response.status_code == ACCESS_ERROR_CODE

def test_sethandle_invalid_user():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    sethandle_response = requests.put(f"{config.url}user/profile/sethandle/v1", json={'token': generate_jwt(99), 'handle_str': "imsocool"})
    assert sethandle_response.status_code == ACCESS_ERROR_CODE

def test_sethandle_simple():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response1.status_code == SUCCESS_CODE
    user1_token = auth_response1.json()['token']
    user1_id = auth_response1.json()['auth_user_id']

    sethandle_response = requests.put(f"{config.url}user/profile/sethandle/v1", json={'token': user1_token, 'handle_str': 'imsocool'})
    assert sethandle_response.status_code == SUCCESS_CODE

    user_response = requests.get(f"{config.url}user/profile/v1", params={'token': user1_token, 'u_id': user1_id})
    assert user_response.status_code == SUCCESS_CODE
    profile = user_response.json()['user']

    assert profile['handle_str'] == 'imsocool'

def test_sethandle_too_short():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response1.status_code == SUCCESS_CODE
    user1_token = auth_response1.json()['token']

    sethandle_response = requests.put(f"{config.url}user/profile/sethandle/v1", json={'token': user1_token, 'handle_str': 'im'})
    assert sethandle_response.status_code == INPUT_ERROR_CODE

def test_sethandle_too_long():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response1.status_code == SUCCESS_CODE
    user1_token = auth_response1.json()['token']

    sethandle_response = requests.put(f"{config.url}user/profile/sethandle/v1", json={'token': user1_token, 'handle_str': '123456789012345678901'})
    assert sethandle_response.status_code == INPUT_ERROR_CODE

def test_sethandle_not_alnum():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response1.status_code == SUCCESS_CODE
    user1_token = auth_response1.json()['token']

    sethandle_response = requests.put(f"{config.url}user/profile/sethandle/v1", json={'token': user1_token, 'handle_str': 'imso@'})
    assert sethandle_response.status_code == INPUT_ERROR_CODE

def test_sethandle_in_use():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response1.status_code == SUCCESS_CODE
    user1_token = auth_response1.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    
    sethandle_response = requests.put(f"{config.url}user/profile/sethandle/v1", json={'token': user1_token, 'handle_str': 'harveymiao'})
    assert sethandle_response.status_code == INPUT_ERROR_CODE

def test_sethandle_reuse_handle():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response1.status_code == SUCCESS_CODE
    user1_token = auth_response1.json()['token']
    user1_id = auth_response1.json()['auth_user_id']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_id = auth_response2.json()['auth_user_id']

    remove_response = requests.delete(f"{config.url}admin/user/remove/v1",json={'token': user1_token, 'u_id': user2_id})
    assert remove_response.status_code == SUCCESS_CODE
    
    sethandle_response = requests.put(f"{config.url}user/profile/sethandle/v1", json={'token': user1_token, 'handle_str': 'harveymiao'})
    assert sethandle_response.status_code == SUCCESS_CODE

    user_response = requests.get(f"{config.url}user/profile/v1", params={'token': user1_token, 'u_id': user1_id})
    assert user_response.status_code == SUCCESS_CODE
    profile = user_response.json()['user']

    assert profile['handle_str'] == 'harveymiao'