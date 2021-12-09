import requests
from werkzeug.datastructures import Accept
from src import config
import pytest
from src.test_config import *
import time
import datetime

from tests.message_share_http_test import initialize_test 

@pytest.fixture()
def initialize_message_sendlater_test():
    ''''
    channels': [
        {
            'id': 1,
            'name': "Test channel",
            'owner_members': [1],
            'all_members': [1]
            "is_public": True
            'messages': []
        },
        {
            'id': 2,
            'name': "Test channel 2",
            'owner_members': [1],
            'all_members': [1, 2]
            "is_public": True
            'messages': []
        }'''
    # Clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    # Registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user1 = auth_response_1.json()
    user2 = auth_response_2.json()
    
    # Create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1['token'], 'name': 'Test channel', 'is_public': True})
    channel_1 = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id_1 = channel_1['channel_id']

    return {
        'user1': user1,
        'user2': user2,
        'channel_id_1': channel_id_1
        }

def test_message_sendlater_success(initialize_message_sendlater_test):
    
    user_1 = initialize_message_sendlater_test['user1']
    channel_1 = initialize_message_sendlater_test['channel_id_1']
    
    # Send the message after 3 seconds
    dtime = datetime.datetime.now()
    time_sent = int(time.mktime(dtime.timetuple())) + 3
    sendlater_response = requests.post(f"{config.url}message/sendlater/v1",json={'token': user_1['token'], 'channel_id': channel_1, 'message': "Hey folk", "time_sent": time_sent})
    assert sendlater_response.status_code == SUCCESS_CODE
    sent_message = sendlater_response.json()['message_id']

    #Test if the shared message can be removed
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={"token": user_1['token'], "message_id": sent_message })
    assert message_remove_response.status_code == INPUT_ERROR_CODE

    time.sleep(4)
    
    #Test if the shared message can be removed
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={"token": user_1['token'], "message_id": sent_message })
    assert message_remove_response.status_code == SUCCESS_CODE

def test_message_sendlater_invalid_channel_id(initialize_message_sendlater_test):

    user_1 = initialize_message_sendlater_test['user1']
    
    # Send the message after 3 seconds
    dtime = datetime.datetime.now()
    time_sent = int(time.mktime(dtime.timetuple())) + 3
    sendlater_response = requests.post(f"{config.url}message/sendlater/v1",json={'token': user_1['token'], 'channel_id': 3, 'message': "Hey folk", "time_sent": time_sent})
    assert sendlater_response.status_code == INPUT_ERROR_CODE

def test_message_sendlater_over_1000_characters_message(initialize_message_sendlater_test):
    
    user_1 = initialize_message_sendlater_test['user1']
    channel_1 = initialize_message_sendlater_test['channel_id_1']

    # Send the message after 3 seconds
    dtime = datetime.datetime.now()
    time_sent = int(time.mktime(dtime.timetuple())) + 3
    sendlater_response = requests.post(f"{config.url}message/sendlater/v1",json={'token': user_1['token'], 'channel_id': channel_1, 'message': over_1000_characters, "time_sent": time_sent})
    assert sendlater_response.status_code == INPUT_ERROR_CODE

def test_message_sendlater_empty_message(initialize_message_sendlater_test):
    
    user_1 = initialize_message_sendlater_test['user1']
    channel_1 = initialize_message_sendlater_test['channel_id_1']

    # Send the message after 3 seconds
    dtime = datetime.datetime.now()
    time_sent = int(time.mktime(dtime.timetuple())) + 3
    sendlater_response = requests.post(f"{config.url}message/sendlater/v1",json={'token': user_1['token'], 'channel_id': channel_1, 'message': '', "time_sent": time_sent})
    assert sendlater_response.status_code == INPUT_ERROR_CODE

def test_message_sendlater_past_time_sent(initialize_message_sendlater_test):
    
    user_1 = initialize_message_sendlater_test['user1']
    channel_1 = initialize_message_sendlater_test['channel_id_1']
    
    # Send the message after 3 seconds
    dtime = datetime.datetime.now()
    time_sent = int(time.mktime(dtime.timetuple())) - 3
    sendlater_response = requests.post(f"{config.url}message/sendlater/v1",json={'token': user_1['token'], 'channel_id': channel_1, 'message': "Hey folk", "time_sent": time_sent})
    assert sendlater_response.status_code == INPUT_ERROR_CODE

def test_message_sendlater_invalid_token(initialize_message_sendlater_test):
    
    channel_1 = initialize_message_sendlater_test['channel_id_1']
    
    # Send the message after 3 seconds
    dtime = datetime.datetime.now()
    time_sent = int(time.mktime(dtime.timetuple())) + 3
    sendlater_response = requests.post(f"{config.url}message/sendlater/v1",json={'token': invalid_token, 'channel_id': channel_1, 'message': "Hey folk", "time_sent": time_sent})
    assert sendlater_response.status_code == ACCESS_ERROR_CODE


def test_message_sendlater_auth_user_is_not_channel_member(initialize_message_sendlater_test):
    
    user2 = initialize_message_sendlater_test['user2']
    channel_1 = initialize_message_sendlater_test['channel_id_1']
    
    # Send the message after 3 seconds
    dtime = datetime.datetime.now()
    time_sent = int(time.mktime(dtime.timetuple())) + 3
    sendlater_response = requests.post(f"{config.url}message/sendlater/v1",json={'token': user2['token'], 'channel_id': channel_1, 'message': "Hey folk", "time_sent": time_sent})
    assert sendlater_response.status_code == ACCESS_ERROR_CODE
