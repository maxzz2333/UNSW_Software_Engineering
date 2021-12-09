import requests
from src import config
from src.helpers import generate_jwt

ACCESS_ERROR_CODE = 403
INPUT_ERROR_CODE = 400
SUCCESS_CODE = 200
USER_1 = {'email': "z5362100@ad.unsw.edu.au",
         'password': "password", 
         'name_first': "Glenn",
         'name_last': "Deng" }

USER_2 = {'email': "z5191576@ad.unsw.edu.au",
         'password': "password", 
         'name_first': "Harvey",
         'name_last': "Miao" }

def test_listall_invalid_token():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    list_response = requests.get(f"{config.url}channels/listall/v2", params={'token': 'invalidtoken'})
    assert list_response.status_code == ACCESS_ERROR_CODE

def test_listall_invalid_user():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    list_response = requests.get(f"{config.url}channels/listall/v2", params={'token': generate_jwt(99)})
    assert list_response.status_code == ACCESS_ERROR_CODE

def test_listall_simple():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    
    channel_response = requests.post(f"{config.url}channels/create/v2", json={'token': user1_token, 'name': 'channel0', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel0_id = channel_response.json()["channel_id"]

    channel_response1 = requests.post(f"{config.url}channels/create/v2", json={'token': user1_token, 'name': 'channel1', 'is_public': True})
    assert channel_response1.status_code == SUCCESS_CODE
    channel1_id = channel_response1.json()["channel_id"]

    list_response = requests.get(f"{config.url}channels/listall/v2", params={'token': user1_token})
    assert list_response.status_code == SUCCESS_CODE
    list_data = list_response.json()
    
    assert list_data == {
        "channels": [
            {
                "channel_id": channel0_id,
                "name": "channel0"
            },
            {
                "channel_id": channel1_id,
                "name": "channel1"
            }
        ]
    }

def test_listall_none():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    list_response = requests.get(f"{config.url}channels/listall/v2", params={'token': user1_token})
    assert list_response.status_code == SUCCESS_CODE
    list_data = list_response.json()

    assert list_data == {
        "channels": []
    }

def test_listall_mixed():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response1.status_code == SUCCESS_CODE
    user1_token = auth_response1.json()['token']
    
    channel_response0 = requests.post(f"{config.url}channels/create/v2", json={'token': user1_token, 'name': 'channel0', 'is_public': True})
    assert channel_response0.status_code == SUCCESS_CODE
    channel0_id = channel_response0.json()["channel_id"]

    channel_response1 = requests.post(f"{config.url}channels/create/v2", json={'token': user1_token, 'name': 'channel1', 'is_public': False})
    assert channel_response1.status_code == SUCCESS_CODE
    channel1_id = channel_response1.json()["channel_id"]

    channel_response2 = requests.post(f"{config.url}channels/create/v2", json={'token': user1_token, 'name': 'channel2', 'is_public': True})
    assert channel_response2.status_code == SUCCESS_CODE
    channel2_id = channel_response2.json()["channel_id"]

    list_response = requests.get(f"{config.url}channels/listall/v2", params={'token': user1_token})
    assert list_response.status_code == SUCCESS_CODE
    list_data = list_response.json()

    assert list_data == {
        "channels": [
            {
                "channel_id": channel0_id,
                "name": "channel0"
            },
            {
                "channel_id": channel1_id,
                "name": "channel1"
            },
            {
                "channel_id": channel2_id,
                "name": "channel2"
            }
        ]
    }

def test_listall_private():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response1.status_code == SUCCESS_CODE
    user1_token = auth_response1.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2", json={'token': user1_token, 'name': 'channel0', 'is_public': False})
    assert channel_response.status_code == SUCCESS_CODE
    channel0_id = channel_response.json()["channel_id"]

    channel_response1 = requests.post(f"{config.url}channels/create/v2", json={'token': user1_token, 'name': 'channel1', 'is_public': False})
    assert channel_response1.status_code == SUCCESS_CODE
    channel1_id = channel_response1.json()["channel_id"]

    list_response = requests.get(f"{config.url}channels/listall/v2", params={'token': user1_token})
    assert list_response.status_code == SUCCESS_CODE
    list_data = list_response.json()

    assert list_data == {
        "channels": [
            {
                "channel_id": channel0_id,
                "name": "channel0"
            },
            {
                "channel_id": channel1_id,
                "name": "channel1"
            }
        ]
    }
    
def test_listall_different_users():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE
    
    auth_response1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response1.status_code == SUCCESS_CODE
    user1_token = auth_response1.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    channel_response0 = requests.post(f"{config.url}channels/create/v2", json={'token': user1_token, 'name': 'channel0', 'is_public': True})
    assert channel_response0.status_code == SUCCESS_CODE
    channel0_id = channel_response0.json()["channel_id"]

    channel_response1 = requests.post(f"{config.url}channels/create/v2", json={'token': user1_token, 'name': 'channel1', 'is_public': True})
    assert channel_response1.status_code == SUCCESS_CODE
    channel1_id = channel_response1.json()["channel_id"]

    channel_response2 = requests.post(f"{config.url}channels/create/v2", json={'token': user2_token, 'name': 'channel2', 'is_public': True})
    assert channel_response2.status_code == SUCCESS_CODE
    channel2_id = channel_response2.json()["channel_id"]

    list_response = requests.get(f"{config.url}channels/listall/v2", params={'token': user1_token})
    assert list_response.status_code == SUCCESS_CODE
    list_data = list_response.json()

    assert list_data == {
        "channels": [
            {
                "channel_id": channel0_id,
                "name": "channel0"
            },
            {
                "channel_id": channel1_id,
                "name": "channel1"
            },
            {
                "channel_id": channel2_id,
                "name": "channel2"
            }
        ]
    }
