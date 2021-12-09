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

def test_leave_dm_as_member():
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
    dm1_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id'], user_3['auth_user_id']]})
    assert dm1_response.status_code == SUCCESS_CODE

    dm2_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert dm2_response.status_code == SUCCESS_CODE

    # dm_list before leave
    dm_list_res = requests.get(f"{config.url}dm/list/v1", params={'token': user_2['token']})
    assert dm_list_res.status_code == SUCCESS_CODE
    dm_list_1 = dm_list_res.json()
    assert dm_list_1 == {'dms': [
        {
            'dm_id': 1,
            'name': "catdog, harveymiao, haydensmith"},
        {
            'dm_id': 2,
            'name': "harveymiao, haydensmith"
        }
    ]}

    # user 2 leave the DM 2
    dm_leave_res = requests.post(f"{config.url}dm/leave/v1", json={'token': user_2['token'], 'dm_id': 2})
    assert dm_leave_res.status_code == SUCCESS_CODE

    # dm_list after leave
    dm_list_res = requests.get(f"{config.url}dm/list/v1", params={'token': user_2['token']})
    assert dm_list_res.status_code == SUCCESS_CODE
    dm_list_1 = dm_list_res.json()
    assert dm_list_1 == {'dms': [
        {
            'dm_id': 1,
            'name': "catdog, harveymiao, haydensmith"
        }
    ]}

def test_leave_dm_as_creator():
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
    dm1_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id'], user_3['auth_user_id']]})
    assert dm1_response.status_code == SUCCESS_CODE

    dm2_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert dm2_response.status_code == SUCCESS_CODE

    # dm_list before remove
    dm_list_res = requests.get(f"{config.url}dm/list/v1", params={'token': user_1['token']})
    assert dm_list_res.status_code == SUCCESS_CODE
    dm_list_1 = dm_list_res.json()
    assert dm_list_1 == {'dms': [
        {
            'dm_id': 1,
            'name': "catdog, harveymiao, haydensmith"},
        {
            'dm_id': 2,
            'name': "harveymiao, haydensmith"
        }
    ]}

    # user 2 leave the DM 2
    dm_leave_res = requests.post(f"{config.url}dm/leave/v1", json={'token': user_1['token'], 'dm_id': 1})
    assert dm_leave_res.status_code == SUCCESS_CODE

    # dm_list after remove
    dm_list_res = requests.get(f"{config.url}dm/list/v1", params={'token': user_1['token']})
    assert dm_list_res.status_code == SUCCESS_CODE
    dm_list_1 = dm_list_res.json()
    assert dm_list_1 == {'dms': [
        {
            'dm_id': 2,
            'name': "harveymiao, haydensmith"
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

    # leave the DM with incorrect token
    dm_leave_res = requests.post(f"{config.url}dm/leave/v1", json={'token': "trivialJWT", 'dm_id': 1})
    assert dm_leave_res.status_code == ACCESS_ERROR_CODE


def test_not_exist_session_id():
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

    # leave the DM with incorrect token
    dm_leave_res = requests.post(f"{config.url}dm/leave/v1", json={'token': generate_jwt(user_1['auth_user_id'], 15), 'dm_id': 1})
    assert dm_leave_res.status_code == ACCESS_ERROR_CODE

def test_not_exist_dm_id():
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

    # leave the DM with incorrect token
    dm_leave_res = requests.post(f"{config.url}dm/leave/v1", json={'token': user_1['token'], 'dm_id': 8})
    assert dm_leave_res.status_code == INPUT_ERROR_CODE

def test_auth_user_is_not_member_of_dm():
    clear_res = requests.delete(f"{config.url}clear/v1")
    assert clear_res.status_code == SUCCESS_CODE

    # Register 2 users
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

    # leave the DM with incorrect token
    dm_leave_res = requests.post(f"{config.url}dm/leave/v1", json={'token': user_3['token'], 'dm_id': 1})
    assert dm_leave_res.status_code == ACCESS_ERROR_CODE