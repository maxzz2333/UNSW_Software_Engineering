import requests
from src import config

ACCESS_ERROR_CODE = 403
INPUT_ERROR_CODE = 400
SUCCESS_CODE = 200
USER_1 = {'email': "hao.chen908@gmail.com",
         'password': "Somepassword", 
         'name_first': "Harvey",
         'name_last': "Miao" }

def test_passwordreset_request_unregistered_email():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    reset_response = requests.post(f"{config.url}auth/passwordreset/request/v1", json={'email': 'aaaaa@aaaa.com'})
    assert reset_response.status_code == SUCCESS_CODE

def test_passwordreset_request_user_logged_out():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    reset_response = requests.post(f"{config.url}auth/passwordreset/request/v1", json={'email': 'hao.chen908@gmail.com'})
    assert reset_response.status_code == SUCCESS_CODE

    users_response = requests.get(f"{config.url}users/all/v1", params= {'token': user1_token})
    assert users_response.status_code == ACCESS_ERROR_CODE
