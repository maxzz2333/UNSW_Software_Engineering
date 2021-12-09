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
USER_3 = {"email": "z7654321@ad.unsw.edu.au",
         "password": "nopassword", 
         "name_first": "Cat",
         "name_last": "Dog" }

def test_list_single_DM():
    clear_res = requests.delete(f"{config.url}clear/v1")
    assert clear_res.status_code == SUCCESS_CODE

    # Register 2 users
    register1_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert register1_response.status_code == SUCCESS_CODE 
    user_1 = register1_response.json()
    register2_response = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert register2_response.status_code == SUCCESS_CODE
    user_2 = register2_response.json()

    # Create new DM
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE

    # Test creator
    dm_list_res = requests.get(f"{config.url}dm/list/v1", params={'token': user_1['token']})
    assert dm_list_res.status_code == SUCCESS_CODE
    dm_list_1 = dm_list_res.json()
    assert dm_list_1 == {'dms': [{
        'dm_id': 1,
        'name': "harveymiao, haydensmith"}
    ]}

    # Test dm_list
    dm_list_res = requests.get(f"{config.url}dm/list/v1", params={'token': user_2['token']})
    assert dm_list_res.status_code == SUCCESS_CODE
    dm_list_1 = dm_list_res.json()
    assert dm_list_1 == {'dms': [{
        'dm_id': 1,
        'name': "harveymiao, haydensmith"}
    ]}

def test_list_multi_DMs():
    clear_res = requests.delete(f"{config.url}clear/v1")
    assert clear_res.status_code == SUCCESS_CODE

    # Register 3 users
    register1_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert register1_response.status_code == SUCCESS_CODE 
    user_1 = register1_response.json()
    register2_response = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert register2_response.status_code == SUCCESS_CODE
    user_2 = register2_response.json()
    register3_response = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    assert register3_response.status_code == SUCCESS_CODE
    user_3 = register3_response.json()

    # Create new DM
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_2['token'], 
        'u_ids': [user_1['auth_user_id'], user_3['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE

    # Test dm_list
    dm_list_res = requests.get(f"{config.url}dm/list/v1", params={'token': user_2['token']})
    assert dm_list_res.status_code == SUCCESS_CODE
    dm_list_1 = dm_list_res.json()
    assert dm_list_1 == {'dms': [
        {
            'dm_id': 1,
            'name': "harveymiao, haydensmith"
        },
        {
            'dm_id': 2,
            'name': "catdog, harveymiao, haydensmith"
        }
    ]}

def test_broken_token():
    clear_res = requests.delete(f"{config.url}clear/v1")
    assert clear_res.status_code == SUCCESS_CODE

    # Register 2 users
    register1_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert register1_response.status_code == SUCCESS_CODE 
    user_1 = register1_response.json()
    register2_response = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert register2_response.status_code == SUCCESS_CODE
    user_2 = register2_response.json()

    # Create new DM
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE

    # Test with invalid token
    dm_list_res = requests.get(f"{config.url}dm/list/v1", params={'token': "cannotencodedJWT"})
    assert dm_list_res.status_code == ACCESS_ERROR_CODE

def test_dm_list_invalid_session_id():
    clear_res = requests.delete(f"{config.url}clear/v1")
    assert clear_res.status_code == SUCCESS_CODE

    # Register 2 users
    register1_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert register1_response.status_code == SUCCESS_CODE 
    user_1 = register1_response.json()
    register2_response = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert register2_response.status_code == SUCCESS_CODE
    user_2 = register2_response.json()

    # Create new DM
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE

    # Test with invalid token
    dm_list_res = requests.get(f"{config.url}dm/list/v1", params={'token': generate_jwt(user_1['auth_user_id'], 10)})
    assert dm_list_res.status_code == ACCESS_ERROR_CODE

def test_not_a_member_of_any_DMs():
    clear_res = requests.delete(f"{config.url}clear/v1")
    assert clear_res.status_code == SUCCESS_CODE

    # Register 3 users
    register1_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert register1_response.status_code == SUCCESS_CODE 
    user_1 = register1_response.json()
    register2_response = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert register2_response.status_code == SUCCESS_CODE
    user_2 = register2_response.json()
    register3_response = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    assert register3_response.status_code == SUCCESS_CODE
    user_3 = register3_response.json()

    # Create new DM
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE

    # Test dm_list
    dm_list_res = requests.get(f"{config.url}dm/list/v1", params={'token': user_3['token']})
    assert dm_list_res.status_code == SUCCESS_CODE
    dm_list_1 = dm_list_res.json()
    assert dm_list_1 == {'dms': [] }