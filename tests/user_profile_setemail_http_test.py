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

def test_setemail_invalid_token():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    setemail_response = requests.put(f"{config.url}user/profile/setemail/v1", json={'token': 'invalidtoken', 'email': "z5191576@ad.unsw.edu.au"})
    assert setemail_response.status_code == ACCESS_ERROR_CODE

def test_setemail_invalid_user():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    setemail_response = requests.put(f"{config.url}user/profile/setemail/v1", json={'token': generate_jwt(99), 'email': "z5191576@ad.unsw.edu.au"})
    assert setemail_response.status_code == ACCESS_ERROR_CODE

def test_setemail_simple():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']

    setemail_response = requests.put(f"{config.url}user/profile/setemail/v1", json={'token': user1_token, 'email': 'z1234567@ad.unsw.edu.au'})
    assert setemail_response.status_code == SUCCESS_CODE

    user_response = requests.get(f"{config.url}user/profile/v1", params={'token': user1_token, 'u_id': user1_id})
    assert user_response.status_code == SUCCESS_CODE
    profile = user_response.json()['user']

    assert profile['email'] == 'z1234567@ad.unsw.edu.au'

def test_setemail_invalid_email():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    setemail_response = requests.put(f"{config.url}user/profile/setemail/v1", json={'token': user1_token, 'email': 'niceemail'})
    assert setemail_response.status_code == INPUT_ERROR_CODE

def test_setemail_in_use():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response1.status_code == SUCCESS_CODE
    user1_token = auth_response1.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE

    setemail_response = requests.put(f"{config.url}user/profile/setemail/v1", json={'token': user1_token, 'email': 'z5191576@ad.unsw.edu.au'})
    assert setemail_response.status_code == INPUT_ERROR_CODE

def test_setemail_reuse_email():
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

    setemail_response = requests.put(f"{config.url}user/profile/setemail/v1", json={'token': user1_token, 'email': 'z5191576@ad.unsw.edu.au'})
    assert setemail_response.status_code == SUCCESS_CODE

    user_response = requests.get(f"{config.url}user/profile/v1", params={'token': user1_token, 'u_id': user1_id})
    assert user_response.status_code == SUCCESS_CODE
    profile = user_response.json()['user']

    assert profile['email'] == 'z5191576@ad.unsw.edu.au'
