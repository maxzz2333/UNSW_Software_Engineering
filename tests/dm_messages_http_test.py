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


less_1_characters = ''
equal_1_characters = '1'
less_1000_over_1_characters  = 'comp1531'

'''
InputError，
      dm_id does not refer to a valid DM
      or
      start is greater than the total number of messages in the channel
AccessError，
      dm_id is valid and the authorised user is not a member of the DM
'''

def test_dm_messages_token_invalid():
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

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': 0, 'dm_id': dm_id, 'start': 0})
    assert dm_messages_response.status_code == ACCESS_ERROR_CODE

def test_dm_messages_authuser_invalid():
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

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': generate_jwt(user_2['auth_user_id'], 10), 'dm_id': dm_id, 'start': 0})
    assert dm_messages_response.status_code == ACCESS_ERROR_CODE

#Occurrences of InputError channel_id does not refer to a valid dm
def test_dm_messages_dm__id_invalid():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    auth_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response_1.status_code == SUCCESS_CODE
    user1_token = auth_response_1.json()['token']

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user1_token, 'dm_id': -1, 'start': 0})
    assert dm_messages_response.status_code == INPUT_ERROR_CODE

def test_dm_messages_dm__id_invalid_2():
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

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'],'dm_id': -1, 'start': 0})
    assert dm_messages_response.status_code == INPUT_ERROR_CODE


#Occurrences of InputError start is greater than the total number of messages in the channel
def test_dm_messages_get_messages_start_greater_total():
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

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 1})
    assert dm_messages_response.status_code == INPUT_ERROR_CODE


#Occurrences of AccessError dm_id is valid and the authorised user is not a member of the dm
def test_channel_messages_dm_id_valid_user_not_member():
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

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_3['token'], 'dm_id': dm_id, 'start': 1})
    assert dm_messages_response.status_code == ACCESS_ERROR_CODE


#Run successfully
def test_dm_messages_get_messages_empty_start_0():#messages is empty , start == 0.
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

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 0})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    assert dm_messages_data['messages'] == []
    assert dm_messages_data['start'] == 0
    assert dm_messages_data['end'] == -1


#Run successfully
def test_dm_messages_get_messages_no_empty_start_0():#messages has 1 message , start ==0.
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

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 0})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    dm_messages_detail = dm_messages_data['messages']
    messages_0 = dm_messages_detail[0]
    assert messages_0['message_id'] == 1
    assert messages_0['u_id'] == 2
    assert messages_0['message'] == 'comp1531'
    assert dm_messages_data['start'] == 0
    assert dm_messages_data['end'] == -1

def test_dm_messages_get_messages_no_empty_start_0_1():#messages has 1 message , start ==0.
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

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 0})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    dm_messages_detail = dm_messages_data['messages']
    messages_0 = dm_messages_detail[0]
    assert messages_0['message_id'] == 2
    assert messages_0['u_id'] == 2
    assert messages_0['message'] == 'comp1531'
    assert dm_messages_data['start'] == 0
    assert dm_messages_data['end'] == -1


#Run successfully
def test_dm_messages_get_messages_50_start_0():
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
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 0})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    assert len(dm_messages_data['messages']) == 50
    assert dm_messages_data['start'] == 0
    assert dm_messages_data['end'] == 50


#Run successfully
def test_dm_messages_get_messages_50_start_1():
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
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 1})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    assert len(dm_messages_data['messages']) == 49
    assert dm_messages_data['start'] == 1
    assert dm_messages_data['end'] == -1


#Run successfully
def test_dm_messages_get_messages_150_start_50_100_101():
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
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 50})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    assert len(dm_messages_data['messages']) == 50
    assert dm_messages_data['start'] == 50
    assert dm_messages_data['end'] == 100

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 100})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    assert len(dm_messages_data['messages']) == 50
    assert dm_messages_data['start'] == 100
    assert dm_messages_data['end'] == 150

    #get messages
    dm_messages_response = requests.get(f"{config.url}dm/messages/v1",params={'token': user_1['token'], 'dm_id': dm_id, 'start': 101})
    assert dm_messages_response.status_code == SUCCESS_CODE
    dm_messages_data = dm_messages_response.json()
    assert len(dm_messages_data['messages']) == 49
    assert dm_messages_data['start'] == 101
    assert dm_messages_data['end'] == -1