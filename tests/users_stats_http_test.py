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
         "password": "Somepassword", 
         "name_first": "Hayden",
         "name_last": "Smith" }

def test_users_stats_invalid_token():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    users_response = requests.get(f"{config.url}users/stats/v1", params={'token': 'invalidtoken'})
    assert users_response.status_code == ACCESS_ERROR_CODE

def test_user_stats_invalid_user():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    users_response = requests.get(f"{config.url}users/stats/v1", params={'token': generate_jwt(99)})
    assert users_response.status_code == ACCESS_ERROR_CODE

def test_users_stats_basic():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE

    stats_response = requests.get(f"{config.url}users/stats/v1", params={'token': user1_token})
    assert stats_response.status_code == SUCCESS_CODE
    stats_data = stats_response.json()
    assert stats_data['workspace_stats']['utilization_rate'] == 1.0

def test_users_stats_zero():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    stats_response = requests.get(f"{config.url}users/stats/v1", params={'token': user1_token})
    assert stats_response.status_code == SUCCESS_CODE
    stats_data = stats_response.json()
    assert stats_data['workspace_stats']['utilization_rate'] == 0.0
