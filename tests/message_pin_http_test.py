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

equal_1_characters = '1'
less_1000_over_1_characters  = 'comp1531'

'''
InputError when any of:
      
        message_id is not a valid message within a channel or DM that the authorised user has joined
        the message is already pinned
      
AccessError when:
        message_id refers to a valid message in a joined channel/DM and the authorised user does not have owner permissions in the channel/DM
        
'''


def test_message_pin_token_invalid():
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

    #pin message in channel
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': 1, 'message_id': message_id})
    assert message_pin_response.status_code == ACCESS_ERROR_CODE

def test_message_pin_authuser_invalid():
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

    #pin message in channel
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': generate_jwt(user1_id, 10), 'message_id': message_id})
    assert message_pin_response.status_code == ACCESS_ERROR_CODE

#Occurrences of InputError message_id is not a valid message within a channel or DM that the authorised user has joined

def test_message_pin_message_invalid():
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

    #pin message in channel
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': user1_token, 'message_id': -1})
    assert message_pin_response.status_code == INPUT_ERROR_CODE

def test_message_pin_message_already_pinned_in_channel():
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

    #pin message in channel
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': user1_token, 'message_id': message_id})
    assert message_pin_response.status_code == SUCCESS_CODE

    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    channel_messages_detail = channel_messages_data['messages']
    messages_0 = channel_messages_detail[0]
    assert messages_0['message_id'] == message_id
    assert messages_0['is_pinned'] == True

    #pin message in channel
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': user1_token, 'message_id': message_id})
    assert message_pin_response.status_code == INPUT_ERROR_CODE


def test_message_pin_message_already_pinned_in_DM():
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

    #pin message in DM
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': user_1['token'], 'message_id': message_id})
    assert message_pin_response.status_code == SUCCESS_CODE

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 0})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    dm_messages_detail = dm_messages_data['messages']
    messages_0 = dm_messages_detail[0]
    assert messages_0['message_id'] == message_id
    assert messages_0['u_id'] == user_2['auth_user_id']
    assert messages_0['is_pinned'] == True

    #pin message in DM
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': user_1['token'], 'message_id': message_id})
    assert message_pin_response.status_code == INPUT_ERROR_CODE


#Occurrences of AccessError valid message in a joined channel/DM and the authorised user does not have owner permissions in the channel/DM

def test_message_pin_message_valid_user_not_owner_permissions_in_channel():
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

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user3_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id = messages_send_data['message_id']

    #pin message in channel
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': user3_token, 'message_id': message_id})
    assert message_pin_response.status_code == ACCESS_ERROR_CODE

    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user2_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    channel_messages_detail = channel_messages_data['messages']
    messages_0 = channel_messages_detail[0]
    assert messages_0['message_id'] == message_id
    assert messages_0['is_pinned'] == False

def test_message_pin_message_valid_user_not_owner_permissions_in_channel_user_is_golber_owner():
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
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user2_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user3_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id = messages_send_data['message_id']

    #pin message in channel
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': user1_token, 'message_id': message_id})
    assert message_pin_response.status_code == ACCESS_ERROR_CODE

    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user3_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    channel_messages_detail = channel_messages_data['messages']
    messages_0 = channel_messages_detail[0]
    assert messages_0['message_id'] == message_id
    assert messages_0['is_pinned'] == False

def test_message_pin_message_valid_user_not_owner_permissions_in_DM():
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

    #pin message in DM
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': user_2['token'], 'message_id': message_id})
    assert message_pin_response.status_code == ACCESS_ERROR_CODE

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 0})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    dm_messages_detail = dm_messages_data['messages']
    messages_0 = dm_messages_detail[0]
    assert messages_0['message_id'] == message_id
    assert messages_0['u_id'] == user_2['auth_user_id']
    assert messages_0['is_pinned'] == False


#Run successfully in channel 
def test_message_pin_message_valid_user_has_owner_permissions_in_channel():
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

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user3_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id = messages_send_data['message_id']

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user3_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE

    #pin message in channel
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': user1_token, 'message_id': message_id})
    assert message_pin_response.status_code == SUCCESS_CODE

    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    channel_messages_detail = channel_messages_data['messages']
    messages_1 = channel_messages_detail[1]
    assert messages_1['message_id'] == message_id
    assert messages_1['is_pinned'] == True

def test_message_pin_message_valid_user_has_owner_permissions_in_channel_2():
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

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user3_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id = messages_send_data['message_id']

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user3_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE

    #pin message in channel
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': user1_token, 'message_id': message_id})
    assert message_pin_response.status_code == SUCCESS_CODE

    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    channel_messages_detail = channel_messages_data['messages']
    messages_1 = channel_messages_detail[1]
    assert messages_1['message_id'] == message_id
    assert messages_1['is_pinned'] == True


def test_message_pin_message_valid_user_has_owner_permissions_in_channel_user_is_golber_owner():
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
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user2_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user3_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user1_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id = messages_send_data['message_id']

    #pin message in channel
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': user1_token, 'message_id': message_id})
    assert message_pin_response.status_code == SUCCESS_CODE

    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    channel_messages_detail = channel_messages_data['messages']
    messages_0 = channel_messages_detail[0]
    assert messages_0['message_id'] == message_id
    assert messages_0['is_pinned'] == True

#Run successfully in dm
def test_message_pin_message_valid_user_has_owner_permissions_in_dm():
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

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    message_id = messages_senddm_data['message_id']
    
    #pin message in DM
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': user_1['token'], 'message_id': message_id})
    assert message_pin_response.status_code == SUCCESS_CODE

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 0})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    dm_messages_detail = dm_messages_data['messages']
    messages_0 = dm_messages_detail[0]
    assert messages_0['message_id'] == message_id
    assert messages_0['u_id'] == user_2['auth_user_id']
    assert messages_0['is_pinned'] == True
    assert len(dm_messages_data['messages']) == 3
    assert dm_messages_data['start'] == 0
    assert dm_messages_data['end'] == -1


#Run successfully in dm
def test_message_pin_message_valid_user_has_owner_permissions_in_dm_2():
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

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    message_id = messages_senddm_data['message_id']
    
    #pin message in DM
    message_pin_response = requests.post(f"{config.url}message/pin/v1",json={'token': user_1['token'], 'message_id': message_id})
    assert message_pin_response.status_code == SUCCESS_CODE

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 0})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    dm_messages_detail = dm_messages_data['messages']
    messages_0 = dm_messages_detail[0]
    assert messages_0['message_id'] == message_id
    assert messages_0['u_id'] == user_2['auth_user_id']
    assert messages_0['is_pinned'] == True
    assert len(dm_messages_data['messages']) == 3
    assert dm_messages_data['start'] == 0
    assert dm_messages_data['end'] == -1