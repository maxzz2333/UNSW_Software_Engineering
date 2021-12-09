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
      u_id does not refer to a valid user
      or
      u_id refers to a user who is the only global owner
AccessError，
      the authorised user is not a global owner
'''

def test_admin_user_remove_token_invalid():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user_1 = auth_response_1.json()
    user_2 = auth_response_2.json()
    
    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_1['token'], 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user_2['token'], 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user_2['token'], 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    
    #remove user
    remove_response = requests.delete(f"{config.url}admin/user/remove/v1",json={'token': 1, 'u_id': user_2['auth_user_id']})
    assert remove_response.status_code == ACCESS_ERROR_CODE

def test_admin_user_remove_authuser_invalid():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user_1 = auth_response_1.json()
    user_2 = auth_response_2.json()
    
    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_1['token'], 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user_2['token'], 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user_2['token'], 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    
    #remove user
    remove_response = requests.delete(f"{config.url}admin/user/remove/v1",json={'token': generate_jwt(user_1['auth_user_id'], 10), 'u_id': user_2['auth_user_id']})
    assert remove_response.status_code == ACCESS_ERROR_CODE

#Occurrences of InputError
def test_admin_user_remove_uid_invalid():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user_1 = auth_response_1.json()
    user_2 = auth_response_2.json()
    
    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_1['token'], 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user_2['token'], 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user_2['token'], 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    
    #remove user
    remove_response = requests.delete(f"{config.url}admin/user/remove/v1",json={'token': user_1['token'], 'u_id': 3})
    assert remove_response.status_code == INPUT_ERROR_CODE


#Occurrences of InputError
def test_admin_user_is_only_global_owner():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user_1 = auth_response_1.json()
    user_2 = auth_response_2.json()
    
    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_1['token'], 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user_2['token'], 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user_2['token'], 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    
    #remove user
    remove_response = requests.delete(f"{config.url}admin/user/remove/v1",json={'token': user_1['token'], 'u_id': user_1['auth_user_id']})
    assert remove_response.status_code == INPUT_ERROR_CODE


#Occurrences of AccessError
def test_admin_user_is_not_global_owner():
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

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_1['token'], 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user_2['token'], 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user_2['token'], 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    
    #remove user
    remove_response = requests.delete(f"{config.url}admin/user/remove/v1",json={'token': user_2['token'], 'u_id': user_3['auth_user_id']})
    assert remove_response.status_code == ACCESS_ERROR_CODE


#Run successfully
def test_admin_user_is_global_owner():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user_1 = auth_response_1.json()
    user_2 = auth_response_2.json()
    
    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_1['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_1['token'], 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user_2['token'], 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user_2['token'], 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    
    #remove user
    remove_response = requests.delete(f"{config.url}admin/user/remove/v1",json={'token': user_1['token'], 'u_id': user_2['auth_user_id']})
    assert remove_response.status_code == SUCCESS_CODE


#Run successfully
def test_admin_authuser_is_global_owner_user_is_channel_owner():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user_1 = auth_response_1.json()
    user_2 = auth_response_2.json()
    
    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_1['token'], 
        'u_ids': [user_2['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_2['token'], 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user_1['token'], 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user_2['token'], 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    
    #remove user
    remove_response = requests.delete(f"{config.url}admin/user/remove/v1",json={'token': user_1['token'], 'u_id': user_2['auth_user_id']})
    assert remove_response.status_code == SUCCESS_CODE


#Run successfully
def test_admin_user_is_global_owner_user_is_dm_owner():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    auth_response_2 = requests.post(f"{config.url}auth/register/v2", json=USER_2)
    assert auth_response_1.status_code == SUCCESS_CODE
    assert auth_response_2.status_code == SUCCESS_CODE
    user_1 = auth_response_1.json()
    user_2 = auth_response_2.json()
    
    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_2['token'], 
        'u_ids': [user_1['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_1['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_1['token'], 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user_2['token'], 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user_2['token'], 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    
    #remove user
    remove_response = requests.delete(f"{config.url}admin/user/remove/v1",json={'token': user_1['token'], 'u_id': user_2['auth_user_id']})
    assert remove_response.status_code == SUCCESS_CODE


#Run successfully
def test_admin_user_is_global_owner_user_not_join_dm_channel():
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
    user_1 = auth_response_1.json()
    user_2 = auth_response_2.json()
    user_3 = auth_response_3.json()
    
    #create dm
    new_dm_response = requests.post(f"{config.url}dm/create/v1", json={
        'token': user_2['token'], 
        'u_ids': [user_1['auth_user_id']]})
    assert new_dm_response.status_code == SUCCESS_CODE
    dm_id = new_dm_response.json()['dm_id']

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_1['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #create channel
    channel_create_response = requests.post(f"{config.url}channels/create/v2",json={'token': user_1['token'], 'name': 'Test channel', 'is_public': True})
    channel_create_data = channel_create_response.json()
    assert channel_create_response.status_code == SUCCESS_CODE
    channel_id = channel_create_data['channel_id']

    #join user to channel
    channel_join_response = requests.post(f"{config.url}channel/join/v2",json={'token': user_2['token'], 'channel_id': channel_id})
    assert  channel_join_response.status_code == SUCCESS_CODE

    #send message to channel
    message_send_response = requests.post(f"{config.url}message/send/v1",json={'token': user_2['token'], 'channel_id': channel_id, 'message': equal_1_characters})
    assert message_send_response.status_code == SUCCESS_CODE
    
    #remove user
    remove_response = requests.delete(f"{config.url}admin/user/remove/v1",json={'token': user_1['token'], 'u_id': user_3['auth_user_id']})
    assert remove_response.status_code == SUCCESS_CODE