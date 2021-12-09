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

def test_remove_successfully():
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

    # dm_list before remove
    dm_list_res = requests.get(f"{config.url}dm/list/v1", params={'token': user_1['token']})
    assert dm_list_res.status_code == SUCCESS_CODE
    dm_list_1 = dm_list_res.json()
    assert dm_list_1 == {'dms': [{
        'dm_id': 1,
        'name': "harveymiao, haydensmith"}
    ]}

    # remove dm 1
    remove_res = requests.delete(f"{config.url}dm/remove/v1", json={
        'token': user_1['token'],
        'dm_id': 1})
    assert remove_res.status_code == SUCCESS_CODE

    #  dm_list before remove
    dm_list_res = requests.get(f"{config.url}dm/list/v1", params={'token': user_1['token']})
    assert dm_list_res.status_code == SUCCESS_CODE
    dm_list_1 = dm_list_res.json()
    assert dm_list_1 == {'dms': [] }

def test_remove_from_muti_dm():
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

    # Create 2 new DMs
    new_dm1_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm1_response.status_code == SUCCESS_CODE
    new_dm2_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_3['auth_user_id'], user_2['auth_user_id']]})
    assert new_dm2_response.status_code == SUCCESS_CODE

    # dm_list before remove
    dm_list_res = requests.get(f"{config.url}dm/list/v1", params={'token': user_1['token']})
    assert dm_list_res.status_code == SUCCESS_CODE
    dm_list_1 = dm_list_res.json()
    assert dm_list_1 == {'dms': [
        {
            'dm_id': 1,
            'name': "harveymiao, haydensmith"},
        {
            'dm_id': 2,
            'name': "catdog, harveymiao, haydensmith"
        }
    ]}

    # remove dm 1
    remove_res = requests.delete(f"{config.url}dm/remove/v1", json={
        'token': user_1['token'],
        'dm_id': 2})
    assert remove_res.status_code == SUCCESS_CODE

    # dm_list after remove
    dm_list_res = requests.get(f"{config.url}dm/list/v1", params={'token': user_1['token']})
    assert dm_list_res.status_code == SUCCESS_CODE
    dm_list_1 = dm_list_res.json()
    assert dm_list_1 == {'dms': [{
        'dm_id': 1,
        'name': "harveymiao, haydensmith"}
    ]}

def test_dm_id_not_exist():
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

    # remove dm 5
    remove_res = requests.delete(f"{config.url}dm/remove/v1", json={
        'token': user_1['token'],
        'dm_id': 5})
    assert remove_res.status_code == INPUT_ERROR_CODE

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

    # remove dm 5
    remove_res = requests.delete(f"{config.url}dm/remove/v1", json={
        'token': "nonsense",
        'dm_id': 1})
    assert remove_res.status_code == ACCESS_ERROR_CODE

def test_token_of_invalid_session_id():
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

    # remove dm 5
    remove_res = requests.delete(f"{config.url}dm/remove/v1", json={
        'token': generate_jwt(user_1['auth_user_id'], 10),
        'dm_id': 1})
    assert remove_res.status_code == ACCESS_ERROR_CODE

def test_auth_user_is_not_creator():
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

    # remove with user2's token
    remove_res = requests.delete(f"{config.url}dm/remove/v1", json={
        'token': user_2['token'],
        'dm_id': 1})
    assert remove_res.status_code == ACCESS_ERROR_CODE