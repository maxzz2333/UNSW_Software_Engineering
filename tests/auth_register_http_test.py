import requests
from src import config
from src.helpers import generate_jwt, SESSION_TRACKER

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


def test_create_single_user():
    requests.delete(f"{config.url}clear/v1")

    response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user_info = response.json()

    assert response.status_code == SUCCESS_CODE
    assert user_info['auth_user_id'] == 1
    assert user_info['token'] == generate_jwt(1,1)

def test_create_multi_user():
    requests.delete(f"{config.url}clear/v1")

    global SESSION_TRACKER
    user_res_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user_res_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    user_info_1 = user_res_1.json()
    user_info_2 = user_res_2.json()

    assert user_res_1.status_code == SUCCESS_CODE
    assert user_res_2.status_code == SUCCESS_CODE
    assert user_info_1['auth_user_id'] == 1
    assert user_info_2['auth_user_id'] == 2
    assert user_info_1['token'] == generate_jwt(1,1)
    assert user_info_2['token'] == generate_jwt(2,2)

def test_wrong_email_formate():
    requests.delete(f"{config.url}clear/v1")

    response = requests.post(f"{config.url}auth/register/v2", json={
        "email": "z1234567",
        "password": "Somepassword", 
        "name_first": "Hayden",
        "name_last": "Smith" })
    assert response.status_code == INPUT_ERROR_CODE

def test_repeating_email():
    requests.delete(f"{config.url}clear/v1")

    user_res_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user_res_2 = requests.post(f"{config.url}auth/register/v2", json=USER_1)

    assert user_res_1.status_code == SUCCESS_CODE
    assert user_res_2.status_code == INPUT_ERROR_CODE

def test_short_password():
    requests.delete(f"{config.url}clear/v1")
    
    response = requests.post(f"{config.url}auth/register/v2", json={
        "email": "z5191576@ad.unsw.edu.au",
        "password": "pw", 
        "name_first": "Hayden",
        "name_last": "Smith" })
    assert response.status_code == INPUT_ERROR_CODE

def test_invalid_name_first():
    requests.delete(f"{config.url}clear/v1")
    
    response_1 = requests.post(f"{config.url}auth/register/v2", json={
        "email": "z5191576@ad.unsw.edu.au",
        "password": "mypassword", 
        "name_first": "",
        "name_last": "Smith" })
    response_2 = requests.post(f"{config.url}auth/register/v2", json={
        "email": "z1234567@ad.unsw.edu.au",
        "password": "mypassword", 
        "name_first": "poiuyfvjhgcvblkjhgghjklkjhbhjknlNkjnlknlkjblbkcvnklgfghcfbvnbmnjhgjv",
        "name_last": "Smith" })
    assert response_1.status_code == INPUT_ERROR_CODE
    assert response_2.status_code == INPUT_ERROR_CODE

def test_invalid_name_last():
    requests.delete(f"{config.url}clear/v1")
    
    response_1 = requests.post(f"{config.url}auth/register/v2", json={
        "email": "z5191576@ad.unsw.edu.au",
        "password": "mypassword", 
        "name_first": "Hayden",
        "name_last": "" })
    response_2 = requests.post(f"{config.url}auth/register/v2", json={
        "email": "z1234567@ad.unsw.edu.au",
        "password": "mypassword", 
        "name_first": "Hayden",
        "name_last": "poiuyfvjhgcvblkjhgghjklkjhbhjknlNkjnlknlkjblbkcvnklgfghcfbvnbmnjhgjv" })
    assert response_1.status_code == INPUT_ERROR_CODE
    assert response_2.status_code == INPUT_ERROR_CODE

def test_same_user_name():
    requests.delete(f"{config.url}clear/v1")
    response_1 = requests.post(f"{config.url}auth/register/v2", json={
        "email": "z5191576@ad.unsw.edu.au",
        "password": "mypassword", 
        "name_first": "Hayden",
        "name_last": "Smith" })
    response_2 = requests.post(f"{config.url}auth/register/v2", json={
        "email": "z1234567@ad.unsw.edu.au",
        "password": "mypassword", 
        "name_first": "Hayden",
        "name_last": "Smith" })
    response_3 = requests.post(f"{config.url}auth/register/v2", json={
        "email": "z5022222@ad.unsw.edu.au",
        "password": "mypassword", 
        "name_first": "Hayden",
        "name_last": "Smith" })

    assert response_1.status_code == SUCCESS_CODE
    assert response_2.status_code == SUCCESS_CODE
    assert response_3.status_code == SUCCESS_CODE