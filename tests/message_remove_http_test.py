import requests
from src import config
from src.helpers import generate_jwt

ACCESS_ERROR_CODE = 403
INPUT_ERROR_CODE = 400
SUCCESS_CODE = 200

USER_1 = {'email': "z5191576@ad.unsw.edu.au",
         'password': "password", 
         'name_first': "Harvey",
         'name_last': "Miao" }

USER_2 = {'email': "z5355933@ad.unsw.edu.au",
         'password': "123abc!@#", 
         'name_first': "MAX",
         'name_last': "ZHAO" }

USER_3 = {'email': "z535544@ad.unsw.edu.au",
         'password': "123abc!@#", 
         'name_first': "MAX",
         'name_last': "ZHANG" }

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

less_1_characters = ''
equal_1_characters = '1'
equal_1000_characters = 'YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu\
YmGNi2Y1pG3aLIOCmAaczUvhyCSDKdrDUrZK5JDhqAcfWqiBvMniBh8L4htKmogtQx4AfKFaI8SdQLd5GhISkFUlNxhoua0vPiZu'

less_1000_over_1_characters  = 'comp1531'
'''
Given a message_id for a message, this message is removed from the channel/DM

InputError when:
      
        message_id does not refer to a valid message within a channel/DM that the authorised user has joined
      
AccessError when message_id refers to a valid message in a joined channel/DM and none of the following are true:
      
        the message was sent by the authorised user making this request
        the authorised user has owner permissions in the channel/DM
'''
def test_message_remove_token_invalid():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user1_token = auth_response_1.json()['token']
    user2_token = auth_response_2.json()['token']
    
    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id = messages_send_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': 1, 'message_id': message_id})
    assert message_remove_response.status_code == ACCESS_ERROR_CODE 


def test_message_edit_authuser_invalid():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user1_token = auth_response_1.json()['token']
    user2_token = auth_response_2.json()['token']
    user1_id = auth_response_1.json()['auth_user_id']

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id = messages_send_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': generate_jwt(user1_id, 10), 'message_id': message_id})
    assert message_remove_response.status_code == ACCESS_ERROR_CODE     

#Occurrences of InputError  message_id does not refer to a valid message within a channel/DM that the authorised user has joined
def test_message_remove_message_invalid():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user1_token = auth_response_1.json()['token']
    user2_token = auth_response_2.json()['token']
    
    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    assert messages_send_data['message_id'] == 1
    #message_id = messages_send_data['message_id'] 

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user2_token, 'message_id': -1})
    assert message_remove_response.status_code == INPUT_ERROR_CODE

#Occurrences of AccessError the message was not sent by the authorised user making this request and the authorised user not has owner permissions in the channel/DM
def test_message_remove_message_valid_user_not_authorised_and_user_not_channel_owner():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

     #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    auth_response_3 = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    assert auth_response_3.status_code == SUCCESS_CODE
    user1_token = auth_response_1.json()['token']
    user2_token = auth_response_2.json()['token']
    user3_token = auth_response_3.json()['token']
    
    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    assert messages_send_data['message_id'] == 1
    message_id = messages_send_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user3_token, 'message_id': message_id})
    assert message_remove_response.status_code == ACCESS_ERROR_CODE


def test_message_remove_message_valid_user_not_authorised_and_user_not_dm_owner():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    register_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    register_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    register_response_3 = requests.post(f"{config.url}auth/register/v2", json=USER_3)
    assert register_response_1.status_code == SUCCESS_CODE
    assert register_response_2.status_code == SUCCESS_CODE
    assert register_response_3.status_code == SUCCESS_CODE
    user_1 = register_response_1.json()
    user_2 = register_response_2.json()
    user_3 = register_response_3.json()

    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    assert messages_senddm_data['message_id'] == 1
    message_id = messages_senddm_data['message_id'] 

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user_3['token'], 'message_id': message_id})
    assert message_remove_response.status_code == ACCESS_ERROR_CODE

#Run successfully 
def test_message_remove_message_vaild_user_not_authorised_but_user_is_channel_owner():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user1_token = auth_response_1.json()['token']
    user2_token = auth_response_2.json()['token']
    
    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    assert messages_send_data['message_id'] == 1
    message_id = messages_send_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user1_token, 'message_id': message_id})
    assert message_remove_response.status_code == SUCCESS_CODE 

def test_message_remove_message_vaild_user_not_authorised_but_user_is_dm_owner():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    register_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    register_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert register_response_1.status_code == SUCCESS_CODE
    assert register_response_2.status_code == SUCCESS_CODE
    user_1 = register_response_1.json()
    user_2 = register_response_2.json()

    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    assert messages_senddm_data['message_id'] == 1
    message_id = messages_senddm_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user_1['token'], 'message_id': message_id})
    assert message_remove_response.status_code == SUCCESS_CODE 

#Run successfully 
def test_message_remove_message_vaild_user_is_authorised_but_user_not_channel_owner():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user1_token = auth_response_1.json()['token']
    user2_token = auth_response_2.json()['token']
    
    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    assert messages_send_data['message_id'] == 1
    message_id = messages_send_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user2_token, 'message_id': message_id})
    assert message_remove_response.status_code == SUCCESS_CODE 


def test_message_remove_message_vaild_user_is_authorised_but_user_not_dm_owner():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    register_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    register_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert register_response_1.status_code == SUCCESS_CODE
    assert register_response_2.status_code == SUCCESS_CODE
    user_1 = register_response_1.json()
    user_2 = register_response_2.json()

    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    assert messages_senddm_data['message_id'] == 1
    message_id = messages_senddm_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user_2['token'], 'message_id': message_id})
    assert message_remove_response.status_code == SUCCESS_CODE


def test_message_remove_message_vaild_user_is_authorised_but_user_not_dm_owner_2():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    register_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    register_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert register_response_1.status_code == SUCCESS_CODE
    assert register_response_2.status_code == SUCCESS_CODE
    user_1 = register_response_1.json()
    user_2 = register_response_2.json()

    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    assert messages_senddm_data['message_id'] == 1
    message_id = messages_senddm_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user_2['token'], 'message_id': message_id})
    assert message_remove_response.status_code == SUCCESS_CODE

    
#Run successfully 
def test_message_remove_message__user_is_authorised_remove_from_channel_1():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user1_token = auth_response_1.json()['token']
    user2_token = auth_response_2.json()['token']
    
    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    assert messages_send_data['message_id'] == 1
    message_id = messages_send_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user2_token, 'message_id': message_id})
    assert message_remove_response.status_code == SUCCESS_CODE 

    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    assert len(channel_messages_data['messages']) == 0
    assert channel_messages_data['start'] == 0
    assert channel_messages_data['end'] == -1

def test_message_remove_message__user_is_authorised_remove_from_channel_2():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user1_token = auth_response_1.json()['token']
    user2_token = auth_response_2.json()['token']
    
    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel_2', 'is_public': True})
    assert channel_create_response.status_code == SUCCESS_CODE

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']
    
    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    assert messages_send_data['message_id'] == 1
    message_id = messages_send_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user2_token, 'message_id': message_id})
    assert message_remove_response.status_code == SUCCESS_CODE 

    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    assert len(channel_messages_data['messages']) == 0
    assert channel_messages_data['start'] == 0
    assert channel_messages_data['end'] == -1


def test_message_remove_message_user_send_2_messages_remove_1_from_channel():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user1_token = auth_response_1.json()['token']
    user2_token = auth_response_2.json()['token']
    
    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id_1 = messages_send_data['message_id']

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id_2 = messages_send_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user2_token, 'message_id': message_id_1})
    assert message_remove_response.status_code == SUCCESS_CODE 

    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    channel_messages_detail = channel_messages_data['messages']
    messages_0 = channel_messages_detail[0]
    assert messages_0['message_id'] == message_id_2
    assert channel_messages_data['start'] == 0
    assert channel_messages_data['end'] == -1


#Run successfully 
def test_message_remove_message__user_is_authorised_remove_from_dm():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    register_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    register_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert register_response_1.status_code == SUCCESS_CODE
    assert register_response_2.status_code == SUCCESS_CODE
    user_1 = register_response_1.json()
    user_2 = register_response_2.json()

    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    assert messages_senddm_data['message_id'] == 1
    message_id = messages_senddm_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user_2['token'], 'message_id': message_id})
    assert message_remove_response.status_code == SUCCESS_CODE

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 0})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    assert len(dm_messages_data['messages']) == 0
    assert dm_messages_data['start'] == 0
    assert dm_messages_data['end'] == -1

def test_message_remove_message__user_is_authorised_remove_from_dm_2():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    register_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    register_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert register_response_1.status_code == SUCCESS_CODE
    assert register_response_2.status_code == SUCCESS_CODE
    user_1 = register_response_1.json()
    user_2 = register_response_2.json()

    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_2['token'], 
        'u_ids': [user_1['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    assert messages_senddm_data['message_id'] == 1
    message_id = messages_senddm_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user_2['token'], 'message_id': message_id})
    assert message_remove_response.status_code == SUCCESS_CODE

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 0})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    assert len(dm_messages_data['messages']) == 0
    assert dm_messages_data['start'] == 0
    assert dm_messages_data['end'] == -1


def test_message_remove_message_user_send_2_messages_remove_1_from_dm():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    register_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    register_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert register_response_1.status_code == SUCCESS_CODE
    assert register_response_2.status_code == SUCCESS_CODE
    user_1 = register_response_1.json()
    user_2 = register_response_2.json()

    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    message_id_1 = messages_senddm_data['message_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    message_id_2 = messages_senddm_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user_2['token'], 'message_id': message_id_1})
    assert message_remove_response.status_code == SUCCESS_CODE

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 0})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    dm_messages_detail = dm_messages_data['messages']
    messages_0 = dm_messages_detail[0]
    assert messages_0['message_id'] == message_id_2
    assert dm_messages_data['start'] == 0
    assert dm_messages_data['end'] == -1


def test_message_remove_message_user_send_3_messages_remove_1_from_dm():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    register_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    register_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert register_response_1.status_code == SUCCESS_CODE
    assert register_response_2.status_code == SUCCESS_CODE
    user_1 = register_response_1.json()
    user_2 = register_response_2.json()

    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_1['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    message_id_1 = messages_senddm_data['message_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    message_id_3 = messages_senddm_data['message_id']

    #remove message to channel or dm
    message_remove_response = requests.delete(f"{config.url}message/remove/v1",json={'token': user_1['token'], 'message_id': message_id_1})
    assert message_remove_response.status_code == SUCCESS_CODE

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 0})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    dm_messages_detail = dm_messages_data['messages']
    messages_0 = dm_messages_detail[0]
    assert messages_0['message_id'] == message_id_3
    assert dm_messages_data['start'] == 0
    assert dm_messages_data['end'] == -1