import requests
from werkzeug.datastructures import Accept
from src import config
import pytest
from src.test_config import *
import time
import datetime

@pytest.fixture()
def initialize_message_sendlaterdm_test():
    ''''
    'dm': [
        {
            'dm_id': 1
            'name': "haydensmith, haydensmith0"
            'creator': 1
            'member': [1, 2]
            'messages': []
        }
    ]'''
    # Clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    # Registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    auth_response_3 = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    assert auth_response_3.status_code == SUCCESS_CODE
    user1 = auth_response_1.json()
    user2 = auth_response_2.json()
    user3 = auth_response_3.json()
    
    # Create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user1['token'], 
        'u_ids': [user2['auth_user_id']]})
    dm_id = new_dm_response.json()['dm_id']
    assert new_dm_response.status_code == SUCCESS_CODE

    return {
        'user1': user1,
        'user2': user2,
        'user3': user3,
        'dm_id': dm_id
        }

def test_message_sendlaterdm_success(initialize_message_sendlaterdm_test):
    
    user_2 = initialize_message_sendlaterdm_test['user2']
    dm_1 = initialize_message_sendlaterdm_test['dm_id']
    
    # Send the message after 3 seconds
    dtime = datetime.datetime.now()
    time_sent = int(time.mktime(dtime.timetuple())) + 3
    sendlater_response = requests.post(f"{config.url}message/sendlaterdm/v1",json={'token': user_2['token'], 'dm_id': dm_1, 'message': "Hey folk", "time_sent": time_sent})
    assert sendlater_response.status_code == SUCCESS_CODE
    sent_message = sendlater_response.json()['message_id']

    #Test if the shared message can be removed
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={"token": user_2['token'], "message_id": sent_message })
    assert message_remove_response.status_code == INPUT_ERROR_CODE

    time.sleep(4)
    
    #Test if the shared message can be removed
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={"token": user_2['token'], "message_id": sent_message })
    assert message_remove_response.status_code == SUCCESS_CODE

def test_message_sendlaterdm_invalid_dm_id(initialize_message_sendlaterdm_test):

    user_2 = initialize_message_sendlaterdm_test['user1']
    
    # Send the message after 3 seconds
    dtime = datetime.datetime.now()
    time_sent = int(time.mktime(dtime.timetuple())) + 3
    sendlater_response = requests.post(f"{config.url}message/sendlaterdm/v1",json={'token': user_2['token'], 'dm_id': 10, 'message': "Hey folk", "time_sent": time_sent})
    assert sendlater_response.status_code == INPUT_ERROR_CODE

def test_message_sendlater_over_1000_characters_message(initialize_message_sendlaterdm_test):
    
    user_2 = initialize_message_sendlaterdm_test['user1']
    dm_1 = initialize_message_sendlaterdm_test['dm_id']

    # Send the message after 3 seconds
    dtime = datetime.datetime.now()
    time_sent = int(time.mktime(dtime.timetuple())) + 3
    sendlater_response = requests.post(f"{config.url}message/sendlaterdm/v1",json={'token': user_2['token'], 'dm_id': dm_1, 'message': over_1000_characters, "time_sent": time_sent})
    assert sendlater_response.status_code == INPUT_ERROR_CODE

def test_message_sendlater_empty_message(initialize_message_sendlaterdm_test):
    
    user_1 = initialize_message_sendlaterdm_test['user1']
    dm_1 = initialize_message_sendlaterdm_test['dm_id']

    # Send the message after 3 seconds
    dtime = datetime.datetime.now()
    time_sent = int(time.mktime(dtime.timetuple())) + 3
    sendlater_response = requests.post(f"{config.url}message/sendlaterdm/v1",json={'token': user_1['token'], 'dm_id': dm_1, 'message': '', "time_sent": time_sent})
    assert sendlater_response.status_code == INPUT_ERROR_CODE

def test_message_sendlater_past_time_sent(initialize_message_sendlaterdm_test):
    
    user_1 = initialize_message_sendlaterdm_test['user1']
    dm_1 = initialize_message_sendlaterdm_test['dm_id']
    
    # Send the message after 3 seconds
    dtime = datetime.datetime.now()
    time_sent = int(time.mktime(dtime.timetuple())) - 3
    sendlater_response = requests.post(f"{config.url}message/sendlaterdm/v1",json={'token': user_1['token'], 'dm_id': dm_1, 'message': "Hey folk", "time_sent": time_sent})
    assert sendlater_response.status_code == INPUT_ERROR_CODE

def test_message_sendlater_invalid_token(initialize_message_sendlaterdm_test):
    
    dm_1 = initialize_message_sendlaterdm_test['dm_id']
    
    # Send the message after 3 seconds
    dtime = datetime.datetime.now()
    time_sent = int(time.mktime(dtime.timetuple())) + 3
    sendlater_response = requests.post(f"{config.url}message/sendlaterdm/v1",json={'token': invalid_token, 'dm_id': dm_1, 'message': "Hey folk", "time_sent": time_sent})
    assert sendlater_response.status_code == ACCESS_ERROR_CODE

    sendlater_response = requests.post(f"{config.url}message/sendlaterdm/v1",json={'token': "invalid_token", 'dm_id': dm_1, 'message': "Hey folk", "time_sent": time_sent})
    assert sendlater_response.status_code == ACCESS_ERROR_CODE    

def test_message_sendlater_auth_user_is_not_dm_member(initialize_message_sendlaterdm_test):
    
    user3 = initialize_message_sendlaterdm_test['user3']
    dm_1 = initialize_message_sendlaterdm_test['dm_id']
    
    # Send the message after 3 seconds
    dtime = datetime.datetime.now()
    time_sent = int(time.mktime(dtime.timetuple())) + 3
    sendlater_response = requests.post(f"{config.url}message/sendlaterdm/v1",json={'token': user3['token'], 'dm_id': dm_1, 'message': "Hey folk", "time_sent": time_sent})
    assert sendlater_response.status_code == ACCESS_ERROR_CODE
