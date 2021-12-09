import requests
from werkzeug.datastructures import Accept
from src import config
import pytest
from src.test_config import *

@pytest.fixture()
def initialize_test():
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
    channel_id = channel_1['channel_id']

    # User 2 join the channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2['token'], 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    # Create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user1['token'], 
        'u_ids': [user2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    return {'user1': user1,
            'user2': user2,
            'channel_id': channel_id,
            'dm_id': dm_id}

def test_search_single_in_channel(initialize_test):

    user1 = initialize_test['user1']
    user2 = initialize_test['user2']
    channel_id = initialize_test["channel_id"]

    # Send messages to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2['token'], 'channel_id': channel_id, 'message': "Hello world!"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2['token'], 'channel_id': channel_id, 'message': "Bye world!"})
    assert message_send_response.status_code == SUCCESS_CODE

    # Search message
    search_response = requests.get(f"{config.url}search/v1",params={'token': user1['token'], 'query_str': "Bye"})
    assert search_response.status_code == SUCCESS_CODE
    search_messages = search_response.json()['messages']
    assert search_messages[0]['message_id'] == 2
    assert search_messages[0]['u_id'] == 2
    assert search_messages[0]['message'] == "Bye world!"

def test_search_single_in_dm(initialize_test):
    
    user_1 = initialize_test['user1']
    user_2 = initialize_test['user2']
    dm_id = initialize_test["dm_id"]

    # Send messages to dm
    message_senddm_response_1 = requests.post(f"{config.url}message/senddm/v1",json={'token': user_1['token'], 'dm_id': dm_id, 'message': "Hello world!"})
    assert message_senddm_response_1.status_code == SUCCESS_CODE
    message_senddm_response_1 = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': "Goodbye world!"})
    assert message_senddm_response_1.status_code == SUCCESS_CODE

    # Search message
    search_response = requests.get(f"{config.url}search/v1",params={'token': user_1['token'], 'query_str': "bye"})
    assert search_response.status_code == SUCCESS_CODE
    search_messages = search_response.json()['messages']
    assert search_messages[0]['message_id'] == 2
    assert search_messages[0]['u_id'] == 2
    assert search_messages[0]['message'] == "Goodbye world!"

def test_search_seccessive_multiple(initialize_test):

    user1 = initialize_test['user1']
    user2 = initialize_test['user2']
    channel_id = initialize_test["channel_id"]

    # Send messages to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2['token'], 'channel_id': channel_id, 'message': "Hey folk!"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2['token'], 'channel_id': channel_id, 'message': "Hello world!"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2['token'], 'channel_id': channel_id, 'message': "Hello world again!"})
    assert message_send_response.status_code == SUCCESS_CODE

    # Search message
    search_response = requests.get(f"{config.url}search/v1",params={'token': user1['token'], 'query_str': "hello"})
    assert search_response.status_code == SUCCESS_CODE
    search_messages = search_response.json()['messages']
    assert search_messages[0]['message_id'] == 3
    assert search_messages[0]['u_id'] == 2
    assert search_messages[0]['message'] == "Hello world again!"

    assert search_messages[1]['message_id'] == 2
    assert search_messages[1]['u_id'] == 2
    assert search_messages[1]['message'] == "Hello world!"

def test_search_discontinous_multiple(initialize_test):
    user1 = initialize_test['user1']
    user2 = initialize_test['user2']
    channel_id = initialize_test["channel_id"]

    # Send messages to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2['token'], 'channel_id': channel_id, 'message': "Hello world!"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2['token'], 'channel_id': channel_id, 'message': "Hey folk!"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2['token'], 'channel_id': channel_id, 'message': "Hello world again!"})
    assert message_send_response.status_code == SUCCESS_CODE

    # Search message
    search_response = requests.get(f"{config.url}search/v1",params={'token': user1['token'], 'query_str': "Hello"})
    assert search_response.status_code == SUCCESS_CODE
    search_messages = search_response.json()['messages']
    assert search_messages[1]['message_id'] == 1
    assert search_messages[1]['u_id'] == 2
    assert search_messages[1]['message'] == "Hello world!"

    assert search_messages[0]['message_id'] == 3
    assert search_messages[0]['u_id'] == 2
    assert search_messages[0]['message'] == "Hello world again!"

def test_search_invalid_token(initialize_test):
    
    user2 = initialize_test['user2']
    channel_id = initialize_test["channel_id"]

    # Send messages to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2['token'], 'channel_id': channel_id, 'message': "Hello world!"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2['token'], 'channel_id': channel_id, 'message': "Hey folk!"})
    assert message_send_response.status_code == SUCCESS_CODE

    # Search message with invalid token
    search_response = requests.get(f"{config.url}search/v1",params={'token': "wrongtoken", 'query_str': "Hello"})
    assert search_response.status_code == ACCESS_ERROR_CODE

def test_search_over_1000_characters(initialize_test):
    
    user1 = initialize_test['user1']
    user2 = initialize_test['user2']
    channel_id = initialize_test["channel_id"]

    # Send messages to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2['token'], 'channel_id': channel_id, 'message': "Hello world!"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2['token'], 'channel_id': channel_id, 'message': "Hey folk!"})
    assert message_send_response.status_code == SUCCESS_CODE

    # Search message with long query
    search_response = requests.get(f"{config.url}search/v1",params={'token': user1['token'], 'query_str': over_1000_characters})
    assert search_response.status_code == INPUT_ERROR_CODE

def test_search_empty(initialize_test):
    
    user1 = initialize_test['user1']
    user2 = initialize_test['user2']
    channel_id = initialize_test["channel_id"]

    # Send messages to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2['token'], 'channel_id': channel_id, 'message': "Hello world!"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2['token'], 'channel_id': channel_id, 'message': "Hey folk!"})
    assert message_send_response.status_code == SUCCESS_CODE

    # Search message with long query
    search_response = requests.get(f"{config.url}search/v1",params={'token': user1['token'], 'query_str': ''})
    assert search_response.status_code == INPUT_ERROR_CODE
