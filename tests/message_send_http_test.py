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
inputError when:
      
    channel_id does not refer to a valid channel
    length of message is less than 1 or over 1000 characters
    
      
AccessError when:
      
    channel_id is valid and the authorised user is not a member of the channel

'''

def test_message_send_token_invalid():
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': 1, 'channel_id': -1, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == ACCESS_ERROR_CODE


def test_message_send_authuser_invalid():
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': generate_jwt(user1_id, 10), 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == ACCESS_ERROR_CODE


#Occurrences of InputError channel_id does not refer to a valid channel

def test_message_send_channel_id_invalid_no_create_channel():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response_1.status_code == SUCCESS_CODE
    user1_token = auth_response_1.json()['token']

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1_token, 'channel_id': -1, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == INPUT_ERROR_CODE


def test_message_send_channel_id_invalid():
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': -1, 'message': less_1_characters})
    assert message_send_response.status_code == INPUT_ERROR_CODE

#Occurrences of InputError length of message is less than 1

def test_message_send_message_less_1():
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1_characters})
    assert message_send_response.status_code == INPUT_ERROR_CODE


#Occurrences of InputError length of message is ovre than 1000

def test_message_send_message_0ver_1000():
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': over_1000_characters})
    assert message_send_response.status_code == INPUT_ERROR_CODE

#Occurrences of AccessError channel_id is valid and the authorised user is not a member of the channel

def test_message_send_user_not_member():
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

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response.status_code == ACCESS_ERROR_CODE



#Run successfully equal_1000_characters

def test_message_send_message_equal_1000():
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': equal_1000_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    assert messages_send_data['message_id'] == 1



#Run successfully equal_1_characters

def test_message_send_message_equal_1():
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


#Run successfully less1000_over1_characters

def test_message_send_message_less_1000_over_1():
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
    messages_send_data = message_send_response.json()
    assert messages_send_data['message_id'] == 1



#Run successfully less1000_over1_characters

def test_message_send_2_message_less_1000_over_1():
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
    message_send_response_1 = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response_1.status_code == SUCCESS_CODE
    messages_send_data = message_send_response_1.json()
    assert messages_send_data['message_id'] == 1

    message_send_response_2 = requests.post(f"{config.url}message/send/v1",json={'token': user1_token, 'channel_id': channel_id, 'message': less_1000_over_1_characters})
    assert message_send_response_2.status_code == SUCCESS_CODE
    messages_send_data = message_send_response_2.json()
    assert messages_send_data['message_id'] == 2
