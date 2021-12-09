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

def test_channel_detail_simple():
    requests.delete(f"{config.url}clear/v1")

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user_token = auth_response.json()['token']
    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_token, 'name': 'Test channel', 'is_public': True})
    c_id = channel_response.json()['channel_id']

    detail_response = requests.get(f"{config.url}channel/details/v2", params={'token': user_token, 'channel_id': c_id})
    channel_detail = detail_response.json()

    assert channel_detail['name'] == "Test channel"
    assert channel_detail['is_public'] == True
    assert channel_detail['owner_members'] == [{
                'u_id': 1,
                'email': 'z5191576@ad.unsw.edu.au',
                'name_first': 'Harvey',
                'name_last': 'Miao',
                'handle_str': 'harveymiao',
                'profile_img_url': config.url + 'static/default.jpg'
            }]
    assert channel_detail['all_members'] == [{
                'u_id': 1,
                'email': 'z5191576@ad.unsw.edu.au',
                'name_first': 'Harvey',
                'name_last': 'Miao',
                'handle_str': 'harveymiao',
                'profile_img_url': config.url + 'static/default.jpg'
            }]

def test_channel_detail_broken_token():
    requests.delete(f"{config.url}clear/v1")

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user_token = auth_response.json()['token']
    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_token, 'name': 'Test channel', 'is_public': True})
    c_id = channel_response.json()['channel_id']

    detail_response = requests.get(f"{config.url}channel/details/v2", params={'token': 'wrongtoken', 'channel_id': c_id})
    
    assert detail_response.status_code == ACCESS_ERROR_CODE

def test_channel_detail_token_with_invalid_session_id():
    requests.delete(f"{config.url}clear/v1")

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user_token = auth_response.json()['token']
    user_id = auth_response.json()['auth_user_id']
    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_token, 'name': 'Test channel', 'is_public': True})
    c_id = channel_response.json()['channel_id']

    detail_response = requests.get(f"{config.url}channel/details/v2", params={'token': generate_jwt(user_id, 10), 'channel_id': c_id})
    assert detail_response.status_code == ACCESS_ERROR_CODE

def test_channel_id_not_exist():
    requests.delete(f"{config.url}clear/v1")

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user_token = auth_response.json()['token']
    requests.post(f"{config.url}channels/create/v2",json={'token': user_token, 'name': 'Test channel', 'is_public': True})

    detail_response = requests.get(f"{config.url}channel/details/v2", params={'token': user_token, 'channel_id': 2})

    assert detail_response.status_code == INPUT_ERROR_CODE

def test_user_is_not_a_member_of_channel():
    requests.delete(f"{config.url}clear/v1")

    auth1_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    user1_token = auth1_response.json()['token']
    auth2_response = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    user2_token = auth2_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    c_id = channel_response.json()['channel_id']

    detail_response = requests.get(f"{config.url}channel/details/v2", params={'token': user2_token, 'channel_id': c_id})

    assert detail_response.status_code == ACCESS_ERROR_CODE
