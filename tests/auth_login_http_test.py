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

def test_success_login():
    requests.delete(f"{config.url}clear/v1")

    register_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user_1 = register_response.json()
    login_response = requests.post(f"{config.url}auth/login/v2", json={'email':USER_1["email"], "password": USER_1["password"]})
    user_2 = login_response.json()

    assert login_response.status_code == SUCCESS_CODE
    assert user_1['auth_user_id'] == user_2['auth_user_id']
    assert user_2['token'] == generate_jwt(1,2)

def test_email_not_exist():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    requests.post(f"{config.url}auth/register/v2", json=USER_1)
    login_response = requests.post(f"{config.url}auth/login/v2", json={'email':USER_2["email"], "password": USER_1["password"]})
    
    assert login_response.status_code == INPUT_ERROR_CODE

def test_incorrect_password():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    requests.post(f"{config.url}auth/register/v2", json=USER_1)
    login_response = requests.post(f"{config.url}auth/login/v2", json={'email':USER_1["email"], "password": USER_2["password"]})
    
    assert login_response.status_code == INPUT_ERROR_CODE

def test_removed_user():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    # Register 2 users, user_1 is the global owner
    register1_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert register1_response.status_code == SUCCESS_CODE
    register2_response = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert register2_response.status_code == SUCCESS_CODE
    user_2 = register2_response.json()

    login_response = requests.post(f"{config.url}auth/login/v2", json={'email':USER_1["email"], "password": USER_1["password"]})
    assert login_response.status_code == SUCCESS_CODE
    user_1 = login_response.json()

    remove_response = requests.delete(f"{config.url}admin/user/remove/v1",json={'token': user_1['token'], 'u_id': user_2['auth_user_id']})
    assert remove_response.status_code == SUCCESS_CODE

    login_response = requests.post(f"{config.url}auth/login/v2", json={'email':USER_2["email"], "password": USER_2["password"]})
    assert login_response.status_code == ACCESS_ERROR_CODE