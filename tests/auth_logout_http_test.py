import requests
from src import config
from src.helpers import generate_jwt


ACCESS_ERROR_CODE = 403
INPUT_ERROR_CODE = 400
SUCCESS_CODE = 200
USER_1 = {'email': "z5191576@ad.unsw.edu.au",
         'password': "Somepassword", 
         'name_first': "Harvey",
         'name_last': "Miao" }
USER_2 = {"email": "z1234567@ad.unsw.edu.au",
         "password": "nopassword", 
         "name_first": "Hayden",
         "name_last": "Smith" }
less_1000_over_1_characters  = 'comp1531'

def test_success_logout_register_and_login_user():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user_2_token = auth_response_2.json()['token']
    
    #login user
    login_response = requests.post(f"{config.url}auth/login/v2", json={'email':USER_1["email"], "password": USER_1["password"]})
    user_1_token  = login_response.json()['token']

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user_2_token , 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #logout user
    logout_response_1 = requests.post(f"{config.url}auth/logout/v1", json={'token':user_1_token})
    assert logout_response_1.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user_1_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == ACCESS_ERROR_CODE

    #logout user
    logout_response_2 = requests.post(f"{config.url}auth/logout/v1", json={'token':user_2_token })
    assert logout_response_2.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user_2_token , 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == ACCESS_ERROR_CODE

def test_success_logout_login_user():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response_1.status_code == SUCCESS_CODE

    #login user
    login_response = requests.post(f"{config.url}auth/login/v2", json={'email':USER_1["email"], "password": USER_1["password"]})
    user_1_token  = login_response.json()['token']

    #logout user
    logout_response_1 = requests.post(f"{config.url}auth/logout/v1", json={'token':user_1_token})
    assert logout_response_1.status_code == SUCCESS_CODE

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_create_response.status_code == ACCESS_ERROR_CODE


def test_success_logout_register_user():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response_1.status_code == SUCCESS_CODE
    user_1_token  = auth_response_1.json()['token']

    #logout user
    logout_response_1 = requests.post(f"{config.url}auth/logout/v1", json={'token':user_1_token})
    assert logout_response_1.status_code == SUCCESS_CODE

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_create_response.status_code == ACCESS_ERROR_CODE


def test_fail_logout_():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #logout user
    logout_response_1 = requests.post(f"{config.url}auth/logout/v1", json={'token':1})
    assert logout_response_1.status_code == ACCESS_ERROR_CODE

def test_fail_logout_invalid_user():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    logout_response_1 = requests.post(f"{config.url}auth/logout/v1", json={'token':generate_jwt(99)})
    assert logout_response_1.status_code == ACCESS_ERROR_CODE
