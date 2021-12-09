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
USER_3 = {"email": "z0000007@ad.unsw.edu.au",
         "password": "nopassword", 
         "name_first": "Shili",
         "name_last": "Wang" }

def test_create_new_dm_sucessfully():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    register_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user_1 = register_response.json()
    register_response = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    user_2 = register_response.json()
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    dm_id = new_dm_response.json()['dm_id']
    assert new_dm_response.status_code == SUCCESS_CODE
    assert dm_id == 1

def test_create_multi_dm():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    register_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user_1 = register_response.json()
    register_response = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    user_2 = register_response.json()
    register_response = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    user_3 = register_response.json()

    new_dm1_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_3['token'], 
        'u_ids': [user_2['auth_user_id'], user_1['auth_user_id']]})
    dm1_info = new_dm1_response.json()
    assert new_dm1_response.status_code == SUCCESS_CODE

    new_dm2_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_3['auth_user_id']]})
    dm2_info = new_dm2_response.json()
    assert new_dm2_response.status_code == SUCCESS_CODE

    assert dm1_info['dm_id'] == 1
    assert dm2_info['dm_id'] == 2

def test_invalid_token():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    register_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user_1 = register_response.json()

    new_dm1_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': "cannotDecodedJwt", 
        'u_ids': [user_1['auth_user_id']]})

    assert new_dm1_response.status_code == ACCESS_ERROR_CODE

    new_dm2_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': generate_jwt(user_1['auth_user_id'], 2), 
        'u_ids': [user_1['auth_user_id']]})

    assert new_dm2_response.status_code == ACCESS_ERROR_CODE

def test_uids_not_exist():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    register_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user_1 = register_response.json()
    register_response = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    user_2 = register_response.json()

    new_dm1_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [5, 6]})

    assert new_dm1_response.status_code == INPUT_ERROR_CODE

    new_dm1_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id'], 6]})

    assert new_dm1_response.status_code == INPUT_ERROR_CODE
