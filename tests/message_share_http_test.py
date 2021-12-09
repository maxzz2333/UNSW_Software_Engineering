import requests
from werkzeug.datastructures import Accept
from src import config
import pytest
from src.test_config import *

@pytest.fixture()
def initialize_test():
    '''
    'channels': [
        {
            'id': 1,
            'name': "Test channel",
            'owner_members': [1],
            'all_members': [1, 2, 3]
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
        }
    'dm': [
        {
            'dm_id': 1
            'name': "harveymiao, haydensmith, maxzhao"
            'creator': 1
            'member': [1, 2, 3]
            'messages': []
        },
        {
            'dm_id': 2
            'name': "harveymiao, haydensmith"
            'creator': 1
            'member': [1, 2]
            'messages': []
        }
    ]
    '''

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

    # Create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1['token'], 'name': 'Test channel', 'is_public': True})
    channel_1 = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id_1 = channel_1['channel_id']
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1['token'], 'name': 'Test channel 2', 'is_public': True})
    channel_2 = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id_2 = channel_2['channel_id']

    # User 2 join the channels
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2['token'], 'channel_id': channel_id_1})
    assert  channel_join_response.status_code == SUCCESS_CODE
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2['token'], 'channel_id': channel_id_2})
    assert  channel_join_response.status_code == SUCCESS_CODE

    # User 3 join channel 1
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user3['token'], 'channel_id': channel_id_1})
    assert  channel_join_response.status_code == SUCCESS_CODE

    # Create two dms
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user1['token'], 
        'u_ids': [user2['auth_user_id'], user3['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id_1 = new_dm_response.json()['dm_id']
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user1['token'], 
        'u_ids': [user2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id_2 = new_dm_response.json()['dm_id']

    return {'user1': user1,
            'user2': user2,
            'user3': user3,
            'channel_id_1': channel_id_1,
            'channel_id_2': channel_id_2,
            'dm_id_1': dm_id_1,
            'dm_id_2': dm_id_2}


def test_message_share_from_channel_to_channel(initialize_test):
    
    user1 = initialize_test['user1']
    user2 = initialize_test['user2']
    channel_1 = initialize_test["channel_id_1"]
    channel_2 = initialize_test["channel_id_2"]

    # Send message to channel 1
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1['token'], 'channel_id': channel_1, 'message': "Hellow world"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_id = message_send_response.json()['message_id']

    # Share message to channel 2
    message_share_response = requests.post(f"{config.url}message/share/v1", json=
    {
        "token": user2['token'], 
        "og_message_id": message_id, 
        "message": "",
        "channel_id": channel_2,
        "dm_id": -1})
    assert message_share_response.status_code == SUCCESS_CODE
    new_message_id = message_share_response.json()['shared_message_id']
    assert new_message_id == 2

    # Test if the shared message can be removed
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={"token": user1['token'], "message_id": new_message_id })
    assert message_remove_response.status_code == SUCCESS_CODE

def test_message_share_from_dm_to_dm(initialize_test):
    user1 = initialize_test['user1']
    user2 = initialize_test['user2']
    dm_1 = initialize_test["dm_id_1"]
    dm_2 = initialize_test["dm_id_2"]

    # Send message to dm 2
    message_send_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user1['token'], 'dm_id': dm_2, 'message': "Hellow world"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_id = message_send_response.json()['message_id']

    # Share message to dm 1
    message_share_response = requests.post(f"{config.url}message/share/v1", json=
    {
        "token": user2['token'], 
        "og_message_id": message_id, 
        "message": "",
        "channel_id": -1,
        "dm_id": dm_1})
    assert message_share_response.status_code == SUCCESS_CODE
    new_message_id = message_share_response.json()['shared_message_id']
    assert new_message_id == 2

    # Test if the shared message can be removed
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={"token": user1['token'], "message_id": new_message_id })
    assert message_remove_response.status_code == SUCCESS_CODE

def test_message_share_from_dm_to_channel(initialize_test):
    user1 = initialize_test['user1']
    user2 = initialize_test['user2']
    dm_1 = initialize_test["dm_id_1"]
    channel_2 = initialize_test["channel_id_2"]

    # Send message to dm 1
    message_send_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user2['token'], 'dm_id': dm_1, 'message': "Hellow world"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_id = message_send_response.json()['message_id']

    # Share message to channel 2
    message_share_response = requests.post(f"{config.url}message/share/v1", json=
    {
        "token": user2['token'], 
        "og_message_id": message_id, 
        "message": "",
        "channel_id": channel_2,
        "dm_id": -1})
    assert message_share_response.status_code == SUCCESS_CODE
    new_message_id = message_share_response.json()['shared_message_id']
    assert new_message_id == 2

    # Test if the shared message can be removed
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={"token": user1['token'], "message_id": new_message_id })
    assert message_remove_response.status_code == SUCCESS_CODE

def test_message_share_from_channel_to_dm(initialize_test):
    user1 = initialize_test['user1']
    user2 = initialize_test['user2']
    channel_1 = initialize_test["channel_id_1"]
    dm_2 = initialize_test["dm_id_2"]

    # Send message to channel 1
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1['token'], 'channel_id': channel_1, 'message': "Hellow world"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_id = message_send_response.json()['message_id']

    # Share message to dm 2
    message_share_response = requests.post(f"{config.url}message/share/v1", json=
    {
        "token": user2['token'], 
        "og_message_id": message_id, 
        "message": "",
        "channel_id": -1,
        "dm_id": dm_2})
    assert message_share_response.status_code == SUCCESS_CODE
    new_message_id = message_share_response.json()['shared_message_id']
    assert new_message_id == 2

    # Test if the shared message can be removed
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={"token": user1['token'], "message_id": new_message_id })
    assert message_remove_response.status_code == SUCCESS_CODE

def test_message_share_with_addtional_message(initialize_test):
    
    user1 = initialize_test['user1']
    user2 = initialize_test['user2']
    channel_1 = initialize_test["channel_id_1"]
    channel_2 = initialize_test["channel_id_2"]

    # Send message to channel 1
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1['token'], 'channel_id': channel_1, 'message': "Hellow world"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_id = message_send_response.json()['message_id']

    # Share message to channel 2
    message_share_response = requests.post(f"{config.url}message/share/v1", json=
    {
        "token": user2['token'], 
        "og_message_id": message_id, 
        "message": "Good evening",
        "channel_id": channel_2,
        "dm_id": -1})
    assert message_share_response.status_code == SUCCESS_CODE
    new_message_id = message_share_response.json()['shared_message_id']

    # Test if the shared message can be removed
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={"token": user1['token'], "message_id": new_message_id })
    assert message_remove_response.status_code == SUCCESS_CODE

def test_message_share_invalid_channel_id_and_dm_id(initialize_test):

    user1 = initialize_test['user1']
    user2 = initialize_test['user2']
    channel_1 = initialize_test["channel_id_1"]

    # Send message to channel 1
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1['token'], 'channel_id': channel_1, 'message': "Hellow world"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_id = message_send_response.json()['message_id']

    # Share message to channel 2
    message_share_response = requests.post(f"{config.url}message/share/v1", json=
    {
        "token": user2['token'], 
        "og_message_id": message_id, 
        "message": "",
        "channel_id": 23,
        "dm_id": -1})
    assert message_share_response.status_code == INPUT_ERROR_CODE

def test_message_share_no_minus_one(initialize_test):
    
    user1 = initialize_test['user1']
    user2 = initialize_test['user2']
    channel_1 = initialize_test["channel_id_1"]
    dm_1 = initialize_test['dm_id_1']

    # Send message to channel 1
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1['token'], 'channel_id': channel_1, 'message': "Hellow world"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_id = message_send_response.json()['message_id']

    # Share message to channel 2
    message_share_response = requests.post(f"{config.url}message/share/v1", json=
    {
        "token": user2['token'], 
        "og_message_id": message_id, 
        "message": "",
        "channel_id": channel_1,
        "dm_id": dm_1})
    assert message_share_response.status_code == INPUT_ERROR_CODE

def test_message_share_not_a_member_of_orginial_channel(initialize_test):
    
    user1 = initialize_test['user1']
    user3 = initialize_test['user3']
    channel_1 = initialize_test["channel_id_1"]
    channel_2 = initialize_test["channel_id_2"]

    # Send message to channel 1
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1['token'], 'channel_id': channel_2, 'message': "Hellow world"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_id = message_send_response.json()['message_id']

    # Share message to channel 2
    message_share_response = requests.post(f"{config.url}message/share/v1", json=
    {
        "token": user3['token'], 
        "og_message_id": message_id, 
        "message": "",
        "channel_id": channel_1,
        "dm_id": -1})
    assert message_share_response.status_code == INPUT_ERROR_CODE

def test_message_share_not_a_member_of_orginial_dm(initialize_test):
    
    user1 = initialize_test['user1']
    user3 = initialize_test['user3']
    dm_1 = initialize_test["dm_id_1"]
    dm_2 = initialize_test["dm_id_2"]

    # Send message to dm 2
    message_send_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user1['token'], 'dm_id': dm_2, 'message': "Hellow world"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_id = message_send_response.json()['message_id']

    # Share message to channel 2
    message_share_response = requests.post(f"{config.url}message/share/v1", json=
    {
        "token": user3['token'], 
        "og_message_id": message_id, 
        "message": "",
        "channel_id": -1,
        "dm_id": dm_1})
    assert message_share_response.status_code == INPUT_ERROR_CODE

def test_message_share_not_a_member_of_the_channel_or_dm_to_be_shared(initialize_test):
    
    user1 = initialize_test['user1']
    user3 = initialize_test['user3']
    channel_1 = initialize_test["channel_id_1"]
    channel_2 = initialize_test["channel_id_2"]

    # Send message to channel 2
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1['token'], 'channel_id': channel_1, 'message': "Hellow world"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_id = message_send_response.json()['message_id']

    # Share message to channel 1
    message_share_response = requests.post(f"{config.url}message/share/v1", json=
    {
        "token": user3['token'], 
        "og_message_id": message_id, 
        "message": "",
        "channel_id": channel_2,
        "dm_id": -1})
    assert message_share_response.status_code == ACCESS_ERROR_CODE

def test_message_non_exist_original_message_id(initialize_test):
    user1 = initialize_test['user1']
    user2 = initialize_test['user2']
    channel_1 = initialize_test["channel_id_1"]
    channel_2 = initialize_test["channel_id_2"]

    # Send message to channel 1
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1['token'], 'channel_id': channel_1, 'message': "Hellow world"})
    assert message_send_response.status_code == SUCCESS_CODE

    # Share message to channel 2
    message_share_response = requests.post(f"{config.url}message/share/v1", json=
    {
        "token": user2['token'], 
        "og_message_id": 100, 
        "message": "",
        "channel_id": channel_2,
        "dm_id": -1})
    assert message_share_response.status_code == INPUT_ERROR_CODE

def test_message_share_invalid_token(initialize_test):

    user1 = initialize_test['user1']
    channel_1 = initialize_test["channel_id_1"]
    channel_2 = initialize_test["channel_id_2"]

    # Send message to channel 1
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1['token'], 'channel_id': channel_1, 'message': "Hellow world"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_id = message_send_response.json()['message_id']

    # Share message to channel 2
    message_share_response = requests.post(f"{config.url}message/share/v1", json=
    {
        "token": invalid_token, 
        "og_message_id": message_id, 
        "message": "",
        "channel_id": channel_2,
        "dm_id": -1})
    assert message_share_response.status_code == ACCESS_ERROR_CODE

def test_message_share_message_over_1000_charac(initialize_test):

    user2 = initialize_test['user2']
    dm_1 = initialize_test["dm_id_1"]
    channel_2 = initialize_test["channel_id_2"]

    # Send message to dm 1
    message_send_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user2['token'], 'dm_id': dm_1, 'message': "Hellow world"})
    assert message_send_response.status_code == SUCCESS_CODE
    message_id = message_send_response.json()['message_id']

    # Share message to channel 2
    message_share_response = requests.post(f"{config.url}message/share/v1", json=
    {
        "token": user2['token'], 
        "og_message_id": message_id, 
        "message": over_1000_characters,
        "channel_id": channel_2,
        "dm_id": -1})
    assert message_share_response.status_code == INPUT_ERROR_CODE
    