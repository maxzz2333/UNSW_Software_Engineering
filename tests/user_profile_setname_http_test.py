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

def test_profilesetname_invalid_token():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    setname_response = requests.put(f"{config.url}user/profile/setname/v1", json={'token': 'invalidtoken', 'name_first': 'Hao', 'name_last': 'Chen'})
    assert setname_response.status_code == ACCESS_ERROR_CODE

def test_profilesetname_invalid_user():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    setname_response = requests.put(f"{config.url}user/profile/setname/v1", json={'token': generate_jwt(99), 'name_first': 'Hao', 'name_last': 'Chen'})
    assert setname_response.status_code == ACCESS_ERROR_CODE

def test_profilesetname_simple():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']

    setname_response = requests.put(f"{config.url}user/profile/setname/v1", json={'token': user1_token, 'name_first': 'Hao', 'name_last': 'Chen'})
    assert setname_response.status_code == SUCCESS_CODE

    user_response = requests.get(f"{config.url}user/profile/v1", params={'token': user1_token, 'u_id': user1_id})
    assert user_response.status_code == SUCCESS_CODE
    profile = user_response.json()['user']

    assert profile['name_first'] == 'Hao' and profile['name_last'] == 'Chen'

def test_profilesetname_among_multi_users():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response.status_code == SUCCESS_CODE
    user2_token = auth_response.json()['token']
    user2_id = auth_response.json()['auth_user_id']


    setname_response = requests.put(f"{config.url}user/profile/setname/v1", json={'token': user2_token, 'name_first': 'Hao', 'name_last': 'Chen'})
    assert setname_response.status_code == SUCCESS_CODE

    user_response = requests.get(f"{config.url}user/profile/v1", params={'token': user2_token, 'u_id': user2_id})
    assert user_response.status_code == SUCCESS_CODE
    profile = user_response.json()['user']

    assert profile['name_first'] == 'Hao' and profile['name_last'] == 'Chen'

def test_profilesetname_no_first_name():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    setname_response = requests.put(f"{config.url}user/profile/setname/v1", json={'token': user1_token, 'name_first': '', 'name_last': 'Chen'})
    assert setname_response.status_code == INPUT_ERROR_CODE

def test_profilesetname_too_long_first_name():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    setname_response = requests.put(f"{config.url}user/profile/setname/v1", json={'token': user1_token, 'name_first': 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxy', 'name_last': 'Chen'})
    assert setname_response.status_code == INPUT_ERROR_CODE

def test_profilesetname_no_last_name():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    setname_response = requests.put(f"{config.url}user/profile/setname/v1", json={'token': user1_token, 'name_first': 'Hao', 'name_last': ''})
    assert setname_response.status_code == INPUT_ERROR_CODE

def test_profilesetname_too_long_last_name():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    setname_response = requests.put(f"{config.url}user/profile/setname/v1", json={'token': user1_token, 'name_first': 'Hao', 'name_last': 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxy'})
    assert setname_response.status_code == INPUT_ERROR_CODE

