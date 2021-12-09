import requests
from src import config
from src.helpers import generate_jwt
from src.config import *

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
         "password": "yespassword", 
         "name_first": "Eric",
         "name_last": "Wang" }
USER_4 = {"email": "z8765432@ad.unsw.edu.au",
         "password": "trivialpassword", 
         "name_first": "Lily",
         "name_last": "Huang" }

def test_auth_user_is_DMcreator():
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
    dm_info = new_dm_response.json()

    # ask for detail
    dm_detail_response = requests.get(f"{config.url}dm/details/v1", params={
        'token':user_1['token'],'dm_id': dm_info['dm_id']})
    assert dm_detail_response.status_code == SUCCESS_CODE
    dm_detail = dm_detail_response.json()
    assert dm_detail == {
                            'name': "harveymiao, haydensmith",
                            'members': [
                                {
                                    'u_id': user_1['auth_user_id'],
                                    'email': USER_1["email"],
                                    'name_first': USER_1["name_first"],
                                    'name_last': USER_1["name_last"],
                                    'handle_str': "harveymiao",
                                    'profile_img_url': url + 'static/default.jpg'
                                },
                                {
                                    'u_id': user_2['auth_user_id'],
                                    'email': USER_2["email"],
                                    'name_first': USER_2["name_first"],
                                    'name_last': USER_2["name_last"],
                                    'handle_str': "haydensmith",
                                    'profile_img_url': url + 'static/default.jpg'
                                }
                            ]
                        }


def test_auth_user_is_DMmember():
    clear_res = requests.delete(f"{config.url}clear/v1")
    assert clear_res.status_code == SUCCESS_CODE

    # Register 3 users
    register1_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert register1_response.status_code == SUCCESS_CODE 
    user_1 = register1_response.json()
    register2_response = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert register2_response.status_code == SUCCESS_CODE
    register3_response = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    assert register3_response.status_code == SUCCESS_CODE
    user_3 = register3_response.json()
    register4_response = requests.post(f"{config.url}auth/register/v2", json=USER_4)
    assert register4_response.status_code == SUCCESS_CODE
    user_4 = register4_response.json()

    # Create new DM
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_3['auth_user_id'], user_4['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE

    # ask for detail
    dm_detail_response = requests.get(f"{config.url}dm/details/v1", params={
        'token':user_3['token'],'dm_id': 1})
    assert dm_detail_response.status_code == SUCCESS_CODE
    dm_detail = dm_detail_response.json()
    assert dm_detail == {
                            'name': "ericwang, harveymiao, lilyhuang",
                            'members': [
                                {
                                    'u_id': user_1['auth_user_id'],
                                    'email': USER_1["email"],
                                    'name_first': USER_1["name_first"],
                                    'name_last': USER_1["name_last"],
                                    'handle_str': "harveymiao",
                                    'profile_img_url': url + 'static/default.jpg'
                                },
                                {
                                    'u_id': user_3['auth_user_id'],
                                    'email': USER_3["email"],
                                    'name_first': USER_3["name_first"],
                                    'name_last': USER_3["name_last"],
                                    'handle_str': "ericwang",
                                    'profile_img_url': url + 'static/default.jpg'
                                },
                                {
                                    'u_id': user_4['auth_user_id'],
                                    'email': USER_4["email"],
                                    'name_first': USER_4["name_first"],
                                    'name_last': USER_4["name_last"],
                                    'handle_str': "lilyhuang",
                                    'profile_img_url': url + 'static/default.jpg'
                                }
                            ]
                        }

def test_show_detail_among_multi_DMs():
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

    # Create 2 DMs
    new_dm1_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm1_response.status_code == SUCCESS_CODE
    new_dm2_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id'], user_3['auth_user_id']]})
    assert new_dm2_response.status_code == SUCCESS_CODE

    # ask for detail
    dm_detail_response = requests.get(f"{config.url}dm/details/v1", params={
        'token':user_2['token'],'dm_id': 2})
    assert dm_detail_response.status_code == SUCCESS_CODE
    dm_detail = dm_detail_response.json()
    assert dm_detail == {
                            'name': "ericwang, harveymiao, haydensmith",
                            'members': [
                                {
                                    'u_id': user_1['auth_user_id'],
                                    'email': USER_1["email"],
                                    'name_first': USER_1["name_first"],
                                    'name_last': USER_1["name_last"],
                                    'handle_str': "harveymiao",
                                    'profile_img_url': url + 'static/default.jpg'
                                },
                                {
                                    'u_id': user_2['auth_user_id'],
                                    'email': USER_2["email"],
                                    'name_first': USER_2["name_first"],
                                    'name_last': USER_2["name_last"],
                                    'handle_str': "haydensmith",
                                    'profile_img_url': url + 'static/default.jpg'
                                },
                                {
                                    'u_id': user_3['auth_user_id'],
                                    'email': USER_3["email"],
                                    'name_first': USER_3["name_first"],
                                    'name_last': USER_3["name_last"],
                                    'handle_str': "ericwang",
                                    'profile_img_url': url + 'static/default.jpg'
                                }
                            ]
                        }

def test_dm_details_broken_token():
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

    # ask for detail
    dm_detail_response = requests.get(f"{config.url}dm/details/v1", params={
        'token':"blah", 'dm_id': 1})
    assert dm_detail_response.status_code == ACCESS_ERROR_CODE

def test_dm_details_invalid_session_id():
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

    # ask for detail
    dm_detail_response = requests.get(f"{config.url}dm/details/v1", params={
        'token': generate_jwt(user_1['auth_user_id'], 10), 'dm_id': 1})
    assert dm_detail_response.status_code == ACCESS_ERROR_CODE

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

    # ask for detail
    dm_detail_response = requests.get(f"{config.url}dm/details/v1", params={
        'token': user_1['token'], 'dm_id': 10})
    assert dm_detail_response.status_code == INPUT_ERROR_CODE

def test_auth_user_is_not_DMmember():
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

    # Create 2 DMs
    new_dm1_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm1_response.status_code == SUCCESS_CODE

    # ask for detail
    dm_detail_response = requests.get(f"{config.url}dm/details/v1", params={
        'token':user_3['token'],'dm_id': 1})
    assert dm_detail_response.status_code == ACCESS_ERROR_CODE