import requests
import time
from src import config
from src.helpers import generate_jwt
'''
InputError when any of:
      
        channel_id does not refer to a valid channel
        length of message is over 1000 characters
        an active standup is not currently running in the channel
      
      AccessError when:
      
        channel_id is valid and the authorised user is not a member of the channel
'''

over_1000_characters = 'YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu'

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

def test_standup_send_invalid_channel_id():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']
    
    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': user1_token, 'channel_id': channel_data, 'length': 3})
    assert start_response.status_code == SUCCESS_CODE

    send_response = requests.post(f"{config.url}standup/send/v1",json={'token': user1_token, 'channel_id': 'invalid', 'message': 'abcd'})
    assert send_response.status_code == INPUT_ERROR_CODE

def test_standup_send_massege_too_long():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': user1_token, 'channel_id': channel_data, 'length': 5})
    assert start_response.status_code == SUCCESS_CODE

    send_response = requests.post(f"{config.url}standup/send/v1",json={'token': user1_token, 'channel_id': channel_data, 'message': over_1000_characters})
    assert send_response.status_code == INPUT_ERROR_CODE

def test_standup_send_no_active_standup():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    send_response = requests.post(f"{config.url}standup/send/v1",json={'token': user1_token, 'channel_id': channel_data, 'message': 'abcd'})
    assert send_response.status_code == INPUT_ERROR_CODE

def test_standup_send_auth_user_not_member_of_the_channel():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    auth_response2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response2.status_code == SUCCESS_CODE
    user2_token = auth_response2.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': user1_token, 'channel_id': channel_data, 'length': 5})
    assert start_response.status_code == SUCCESS_CODE

    send_response = requests.post(f"{config.url}standup/send/v1",json={'token': user2_token, 'channel_id': channel_data, 'message': 'abcd'})
    assert send_response.status_code == ACCESS_ERROR_CODE

def test_standup_send_invalid_token():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': user1_token, 'channel_id': channel_data, 'length': 5})
    assert start_response.status_code == SUCCESS_CODE

    send_response = requests.post(f"{config.url}standup/send/v1",json={'token': 'invalid', 'channel_id': channel_data, 'message': 'abcd'})
    assert send_response.status_code == ACCESS_ERROR_CODE 

def test_standup_send_invalid_usr_id():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': user1_token, 'channel_id': channel_data, 'length': 5})
    assert start_response.status_code == SUCCESS_CODE

    send_response = requests.post(f"{config.url}standup/send/v1",json={'token': generate_jwt(user1_token, 2), 'channel_id': channel_data, 'message': 'abcd'})
    assert send_response.status_code == ACCESS_ERROR_CODE 

def test_standup_send_success():
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    channel_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel', 'is_public': True})
    assert channel_response.status_code == SUCCESS_CODE
    channel_data = channel_response.json()['channel_id']

    channel_response2 = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test Channel2', 'is_public': True})
    assert channel_response2.status_code == SUCCESS_CODE
    channel_data = channel_response2.json()['channel_id']

    start_response = requests.post(f"{config.url}standup/start/v1",json={'token': user1_token, 'channel_id': channel_data, 'length': 5})
    assert start_response.status_code == SUCCESS_CODE

    send_response = requests.post(f"{config.url}standup/send/v1",json={'token': user1_token, 'channel_id': channel_data, 'message': 'abcd'})
    assert send_response.status_code == SUCCESS_CODE
