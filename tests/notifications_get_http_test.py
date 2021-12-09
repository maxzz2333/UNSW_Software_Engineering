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

equal_1_chareacters = '1'
valid_chareacters  = 'comp1531'
tagged_user_1 = '@harveymiao hello my friend'
tagged_user_2 = 'hello my friend@maxzhao'
tagged_user_3 = 'hello my@maxzhang friend'
tagged_user_2_and_3 = 'hello my friend@maxzhao and@maxzhang!'



def test_notifications_get_token_invalid():
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1_token, 'channel_id': channel_id, 'message': equal_1_chareacters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id = messages_send_data['message_id']

    #react message in channel
    message_react_response = requests.post(f"{config.url}message/react/v1",json={'token': user2_token, 'message_id': message_id, 'react_id':1})
    assert message_react_response.status_code == SUCCESS_CODE

    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': 1})
    assert notifications_get_response.status_code == ACCESS_ERROR_CODE

def test_notifications_get_authuser_invalid():
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1_token, 'channel_id': channel_id, 'message': equal_1_chareacters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id = messages_send_data['message_id']

    #react message in channel
    message_react_response = requests.post(f"{config.url}message/react/v1",json={'token': user2_token, 'message_id': message_id, 'react_id':1})
    assert message_react_response.status_code == SUCCESS_CODE

    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': generate_jwt(user1_id, 10)})
    assert notifications_get_response.status_code == ACCESS_ERROR_CODE

#Run successfully but no notifications
def test_notifications_get_no_notifications():
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1_token, 'channel_id': channel_id, 'message': equal_1_chareacters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id = messages_send_data['message_id']

    #react message in channel
    message_react_response = requests.post(f"{config.url}message/react/v1",json={'token': user2_token, 'message_id': message_id, 'react_id':1})
    assert message_react_response.status_code == SUCCESS_CODE

    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': user2_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'] == []

#tage invalid - handle invalid
def test_notifications_get_tage_user_handle_invalid():
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': '@harveymiaos hello my friend'})
    assert message_send_response.status_code == SUCCESS_CODE

    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': user1_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'] == []

#tage invalid - taged user not in channel or dm
def test_notifications_get_tage_user_not_in_channel():
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': tagged_user_3})
    assert message_send_response.status_code == SUCCESS_CODE

    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': user3_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'] == []

def test_notifications_get_tage_user_not_in_DM():
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
        'token': user_2['token'], 
        'u_ids': [user_1['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response_1 = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': tagged_user_3})
    assert message_senddm_response_1.status_code == SUCCESS_CODE
    messages_senddm_data_1 = message_senddm_response_1.json()
    assert messages_senddm_data_1['message_id'] == 1

    #get notifications    
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token':  user_3['token']})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'] == []

#Run successfully tage 1 user 
def test_notifications_get_tage_1_user_once_in_channel_send():
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': tagged_user_1})
    assert message_send_response.status_code == SUCCESS_CODE

    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': user1_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'] == [{'channel_id' : 1, 'dm_id' : -1, 'notification_message' : "maxzhao tagged you in Test channel: @harveymiao hello my"}]

def test_notifications_get_tage_1_user_twice_in_channel_send():
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
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user2_token, 'channel_id': channel_id, 'message': '@harveymiao @harveymiao hello my friend'})
    assert message_send_response.status_code == SUCCESS_CODE

    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': user1_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'] == [{'channel_id' : 1, 'dm_id' : -1, 'notification_message' : "maxzhao tagged you in Test channel: @harveymiao @harveym"}]

#Run successfully tage 2 user
def test_notifications_get_tage_2_user_in_channel_send():
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
    user3_id = auth_response_3.json()['auth_user_id']

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #invite user to channel
    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user2_token, 'channel_id': channel_id, 'u_id': user3_id})
    assert invite_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1_token, 'channel_id': channel_id, 'message': tagged_user_2_and_3})
    assert message_send_response.status_code == SUCCESS_CODE

    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': user2_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'] == [{'channel_id' : 1, 'dm_id' : -1, 'notification_message' : "harveymiao tagged you in Test channel: hello my friend@maxz"}]
    
    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': user3_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'][0] == {'channel_id' : 1, 'dm_id' : -1, 'notification_message' : "harveymiao tagged you in Test channel: hello my friend@maxz"}
    assert notifications_get_data['notifications'][1] == {'channel_id' : 1, 'dm_id' : -1, 'notification_message' : "maxzhao added you to Test channel"}

def test_notifications_get_tage_2_user_in_channel_edit():
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
    user3_id = auth_response_3.json()['auth_user_id']

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #invite user to channel
    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user2_token, 'channel_id': channel_id, 'u_id': user3_id})
    assert invite_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1_token, 'channel_id': channel_id, 'message': valid_chareacters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id = messages_send_data['message_id']

    #eid message to channel or dm
    message_edit_response = requests.put(f"{config.url}message/edit/v1",json={'token': user1_token, 'message_id': message_id, 'message': tagged_user_2_and_3})
    assert message_edit_response.status_code == SUCCESS_CODE

    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': user2_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'] == [{'channel_id' : 1, 'dm_id' : -1, 'notification_message' : "harveymiao tagged you in Test channel: hello my friend@maxz"}]
    
    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': user3_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'][0] == {'channel_id' : 1, 'dm_id' : -1, 'notification_message' : "harveymiao tagged you in Test channel: hello my friend@maxz"}
    assert notifications_get_data['notifications'][1] == {'channel_id' : 1, 'dm_id' : -1, 'notification_message' : "maxzhao added you to Test channel"}

def test_notifications_get_tage_2_user_in_channel_share():
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
    user3_id = auth_response_3.json()['auth_user_id']

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #invite user to channel
    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user2_token, 'channel_id': channel_id, 'u_id': user3_id})
    assert invite_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1_token, 'channel_id': channel_id, 'message': valid_chareacters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id = messages_send_data['message_id']

    #create channel2
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel2', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id_2 = channel_create_data['channel_id']

    #join user to channel2
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id_2})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #join user to channel2
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user3_token, 'channel_id': channel_id_2})
    assert  channel_join_response.status_code == SUCCESS_CODE


    # Share message to channel 2
    message_share_response = requests.post(f"{config.url}message/share/v1", json=
    {
        "token": user1_token, 
        "og_message_id": message_id, 
        "message": "@maxzhao@maxzhang",
        "channel_id": channel_id_2,
        "dm_id": -1})
    assert message_share_response.status_code == SUCCESS_CODE


    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': user2_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'] == [{'channel_id' : 2, 'dm_id' : -1, 'notification_message' : "harveymiao tagged you in Test channel2: comp1531\n@maxzhao@ma"}]
    
    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': user3_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'][0] == {'channel_id' : 2, 'dm_id' : -1, 'notification_message' : "harveymiao tagged you in Test channel2: comp1531\n@maxzhao@ma"}
    assert notifications_get_data['notifications'][1] == {'channel_id' : 1, 'dm_id' : -1, 'notification_message' : "maxzhao added you to Test channel"}

#Run successfully tage 1 user once in dm
def test_notifications_get_tage_user_in_dm_send():
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
        'token': user_2['token'], 
        'u_ids': [user_1['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response_1 = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': tagged_user_1})
    assert message_senddm_response_1.status_code == SUCCESS_CODE
    messages_senddm_data_1 = message_senddm_response_1.json()
    assert messages_senddm_data_1['message_id'] == 1

    #get notifications    
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token':  user_1['token']})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'][0] == {'channel_id' : -1, 'dm_id' : 1, 'notification_message' : "maxzhao tagged you in harveymiao, maxzhao: @harveymiao hello my"}
    assert notifications_get_data['notifications'][1] == {'channel_id' : -1, 'dm_id' : 1, 'notification_message' : "maxzhao added you to harveymiao, maxzhao"}


#Run successfully react and invite user in channel
def test_notifications_get_react_and_invite_user_in_channel():
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
    user3_id = auth_response_3.json()['auth_user_id']

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

    #invite user to channel
    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user2_token, 'channel_id': channel_id, 'u_id': user3_id})
    assert invite_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user3_token, 'channel_id': channel_id, 'message': equal_1_chareacters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id = messages_send_data['message_id']

    #ract message in channel
    message_ract_response = requests.post(f"{config.url}message/react/v1",json={'token': user2_token, 'message_id': message_id, 'react_id':1})
    assert message_ract_response.status_code == SUCCESS_CODE

    #get notifications    
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token':  user3_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'][0] == {'channel_id' : 2, 'dm_id' : -1, 'notification_message' : "maxzhao reacted to your message in Test channel"}
    assert notifications_get_data['notifications'][1] == {'channel_id' : 2, 'dm_id' : -1, 'notification_message' : "maxzhao added you to Test channel"}

#react+join+tage
def test_notifications_get_tage_react_join_user_in_channel():
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
    user3_id = auth_response_3.json()['auth_user_id']

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user1_token, 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user2_token, 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #invite user to channel
    invite_response = requests.post(f"{config.url}channel/invite/v2",json={'token': user2_token, 'channel_id': channel_id, 'u_id': user3_id})
    assert invite_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user1_token, 'channel_id': channel_id, 'message': valid_chareacters})
    assert message_send_response.status_code == SUCCESS_CODE
    messages_send_data = message_send_response.json()
    message_id = messages_send_data['message_id']

    #eid message to channel or dm
    message_edit_response = requests.put(f"{config.url}message/edit/v1",json={'token': user1_token, 'message_id': message_id, 'message': tagged_user_2_and_3})
    assert message_edit_response.status_code == SUCCESS_CODE


    #ract message in channel
    message_ract_response = requests.post(f"{config.url}message/react/v1",json={'token': user2_token, 'message_id': message_id, 'react_id':1})
    assert message_ract_response.status_code == SUCCESS_CODE


    #ract message in channel
    message_ract_response = requests.post(f"{config.url}message/react/v1",json={'token': user3_token, 'message_id': message_id, 'react_id':1})
    assert message_ract_response.status_code == SUCCESS_CODE

    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': user1_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'][0] == {'channel_id' : 1, 'dm_id' : -1, 'notification_message' : "maxzhang reacted to your message in Test channel"}
    assert notifications_get_data['notifications'][1] == {'channel_id' : 1, 'dm_id' : -1, 'notification_message' : "maxzhao reacted to your message in Test channel"}

    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': user2_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'] == [{'channel_id' : 1, 'dm_id' : -1, 'notification_message' : "harveymiao tagged you in Test channel: hello my friend@maxz"}]
    
    #get notifications
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token': user3_token})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'][0] == {'channel_id' : 1, 'dm_id' : -1, 'notification_message' : "harveymiao tagged you in Test channel: hello my friend@maxz"}
    assert notifications_get_data['notifications'][1] == {'channel_id' : 1, 'dm_id' : -1, 'notification_message' : "maxzhao added you to Test channel"}


def test_notifications_get_tage_react_join_user_in_dm():
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
        'u_ids': [user_2['auth_user_id'],user_3['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_1['token'], 'dm_id': dm_id, 'message': valid_chareacters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    message_id_1 = messages_senddm_data['message_id']

    #eid message to channel or dm
    message_edit_response = requests.put(f"{config.url}message/edit/v1",json={'token': user_1['token'], 'message_id': message_id_1, 'message': tagged_user_2})
    assert message_edit_response.status_code == SUCCESS_CODE

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_1['token'], 'dm_id': dm_id, 'message': valid_chareacters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    message_id_2 = messages_senddm_data['message_id']

    #eid message to channel or dm
    message_edit_response = requests.put(f"{config.url}message/edit/v1",json={'token': user_1['token'], 'message_id': message_id_2, 'message': tagged_user_3})
    assert message_edit_response.status_code == SUCCESS_CODE
   
    #ract message in channel
    message_ract_response = requests.post(f"{config.url}message/react/v1",json={'token': user_2['token'], 'message_id': message_id_1, 'react_id':1})
    assert message_ract_response.status_code == SUCCESS_CODE

    #ract message in channel
    message_ract_response = requests.post(f"{config.url}message/react/v1",json={'token': user_3['token'], 'message_id': message_id_2, 'react_id':1})
    assert message_ract_response.status_code == SUCCESS_CODE

    #get notifications    
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token':  user_1['token']})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'][0] == {'channel_id' : -1, 'dm_id' : 1, 'notification_message' : "maxzhang reacted to your message in harveymiao, maxzhang, maxzhao"}
    assert notifications_get_data['notifications'][1] == {'channel_id' : -1, 'dm_id' : 1, 'notification_message' : "maxzhao reacted to your message in harveymiao, maxzhang, maxzhao"}
    

    #get notifications    
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token':  user_2['token']})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'][0] == {'channel_id' : -1, 'dm_id' : 1, 'notification_message' : "harveymiao tagged you in harveymiao, maxzhang, maxzhao: hello my friend@maxz"}
    assert notifications_get_data['notifications'][1] == {'channel_id' : -1, 'dm_id' : 1, 'notification_message' : "harveymiao added you to harveymiao, maxzhang, maxzhao"}

    #get notifications    
    notifications_get_response = requests.get(f"{config.url}notifications/get/v1",params={'token':  user_3['token']})
    assert notifications_get_response.status_code == SUCCESS_CODE
    notifications_get_data = notifications_get_response.json()
    assert notifications_get_data['notifications'][0] == {'channel_id' : -1, 'dm_id' : 1, 'notification_message' : "harveymiao tagged you in harveymiao, maxzhang, maxzhao: hello my@maxzhang fr"}
    assert notifications_get_data['notifications'][1] == {'channel_id' : -1, 'dm_id' : 1, 'notification_message' : "harveymiao added you to harveymiao, maxzhang, maxzhao"}