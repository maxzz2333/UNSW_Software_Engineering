import requests
from src import config
from src.helpers import generate_jwt

ACCESS_ERROR_CODE = 403
INPUT_ERROR_CODE = 400
SUCCESS_CODE = 200

less_1_characters = ''
equal_1_characters = '1'
less_1000_over_1_characters  = 'comp1531'

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

'''
InputError，
      channel_id does not refer to a valid channel
      or
      start is greater than the total number of messages in the channel
AccessError，
      channel_id is valid and the authorised user is not a member of the channel
'''

def test_channel_messages_token_invalid():
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

    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': 0, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == ACCESS_ERROR_CODE

def test_channel_messages_authuser_invalid():
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
    user2_id = auth_response_2.json()['auth_user_id']

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': generate_jwt(user2_id, 10), 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == ACCESS_ERROR_CODE

#Occurrences of InputError channel_id does not refer to a valid channel

def test_channel_messages_channel_id_invalid_1():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response_1.status_code == SUCCESS_CODE
    user1_token = auth_response_1.json()['token']

    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': -1, 'start': 0})
    assert channel_messages_response.status_code == INPUT_ERROR_CODE

def test_channel_messages_channel_id_invalid_2():
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
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_create_data = channel_create_response.json()
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user2_token, 'channel_id': -1, 'start': 0})
    assert channel_messages_response.status_code == INPUT_ERROR_CODE

#Occurrences of InputError start is greater than the total number of messages in the channel

def test_channel_messages_get_messages_start_greater_total():
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
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_create_data = channel_create_response.json()
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user2_token, 'channel_id': channel_id, 'start': 100})
    assert channel_messages_response.status_code == INPUT_ERROR_CODE

#Occurrences of AccessError channel_id is valid and the authorised user is not a member of the channel
def test_channel_messages_channel_id_valid_user_not_member_1():
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
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_create_data = channel_create_response.json()
    channel_id = channel_create_data['channel_id']

    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user2_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == ACCESS_ERROR_CODE


def test_channel_messages_channel_id_valid_user_not_member_2():
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

    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user3_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == ACCESS_ERROR_CODE


#Run successfully
def test_channel_messages_get_messages_empty_start_0():#messages is empty , start == 0.
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

    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user2_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()

    assert channel_messages_data['messages'] == []
    assert channel_messages_data['start'] == 0
    assert channel_messages_data['end'] == -1

#Run successfully(channel 
def test_channel_messages_get_messages_not_empty_start_0():#messages is empty , start == 0.
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE

    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    channel_messages_detail = channel_messages_data['messages']
    messages_0 = channel_messages_detail[0]
    assert messages_0['message_id'] == 1
    assert messages_0['u_id'] == 2
    assert messages_0['message'] == 'comp1531'
    assert channel_messages_data['start'] == 0
    assert channel_messages_data['end'] == -1


#Run successfully(channel 
def test_channel_messages_get_messages_not_empty_start_0_1():#messages is empty , start == 0.
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE

    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    channel_messages_detail = channel_messages_data['messages']
    messages_0 = channel_messages_detail[0]
    assert messages_0['message_id'] == 2
    assert messages_0['u_id'] == 2
    assert messages_0['message'] == 'comp1531'
    assert channel_messages_data['start'] == 0
    assert channel_messages_data['end'] == -1


#Run successfully(channel 
def test_channel_messages_get_messages_50_start_0(): 
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE


    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': channel_id, 'start': 0})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    assert len(channel_messages_data['messages']) == 50
    assert channel_messages_data['start'] == 0
    assert channel_messages_data['end'] == 50


#Run successfully(channel 
def test_channel_messages_get_messages_50_start_1(): 
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE


    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': channel_id, 'start': 1})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    assert len(channel_messages_data['messages']) == 49
    assert channel_messages_data['start'] == 1
    assert channel_messages_data['end'] == -1


#Run successfully(channel 
def test_channel_messages_get_messages_150_start_50_100_101(): 
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE


    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE


    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE

    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': channel_id, 'start': 50})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    assert len(channel_messages_data['messages']) == 50
    assert channel_messages_data['start'] == 50
    assert channel_messages_data['end'] == 100

    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': channel_id, 'start': 100})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    assert len(channel_messages_data['messages']) == 50
    assert channel_messages_data['start'] == 100
    assert channel_messages_data['end'] == 150

    #get messages
    channel_messages_response = requests.get(f"{config.url}channel/messages/v2",params={'token': user1_token, 'channel_id': channel_id, 'start': 101})
    assert channel_messages_response.status_code == SUCCESS_CODE
    channel_messages_data = channel_messages_response.json()
    assert len(channel_messages_data['messages']) == 49
    assert channel_messages_data['start'] == 101
    assert channel_messages_data['end'] == -1