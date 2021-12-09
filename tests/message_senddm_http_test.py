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
inputError when:
      
    dm_id does not refer to a valid DM
    length of message is less than 1 or over 1000 characters
    
      
AccessError when:
      
    dm_id is valid and the authorised user is not a member of the DM
'''
def test_message_senddm_dm_token_invalid():
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
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': '', 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == ACCESS_ERROR_CODE

def test_message_senddm_dm_authuser_invalid():
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
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': generate_jwt(user_1['auth_user_id'], 10), 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == ACCESS_ERROR_CODE

#Occurrences of InputError channel_id does not refer to a valid channel

def test_message_senddm_dm_id_invalid():
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

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_1['token'], 'dm_id': -1, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == INPUT_ERROR_CODE


def test_message_senddm_dm_id_invalid_no_create_dm():
    #clear data_store
    response = requests.delete(f"{config.url}clear/v1")
    assert response.status_code == SUCCESS_CODE

    #registered user
    register_response_1 = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert register_response_1.status_code == SUCCESS_CODE  
    user_1 = register_response_1.json()

    #send message to dm
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_1['token'], 'dm_id': -1, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == INPUT_ERROR_CODE


#Occurrences of InputError length of message is ovre than 1000
def test_message_senddm_message_0ver_1000():
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
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_1['token'], 'dm_id': dm_id, 'message': over_1000_characters})
    assert message_senddm_response.status_code == INPUT_ERROR_CODE


#Occurrences of InputError length of message is less than 1
def test_message_senddm_message_less_1():
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
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_1['token'], 'dm_id': dm_id, 'message': less_1_characters})
    assert message_senddm_response.status_code == INPUT_ERROR_CODE


#Occurrences of AccessError  dm_id is valid and the authorised user is not a member of the DM
def test_message_senddm_dm_id_valid_user_not_member():
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
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_3['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response.status_code == ACCESS_ERROR_CODE


#Run successfully equal_1_characters
def test_message_senddm_message_equal_1():
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
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_1['token'], 'dm_id': dm_id, 'message': equal_1_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    assert messages_senddm_data['message_id'] == 1


#Run successfully equal_1000_characters
def test_message_senddm_message_equal_1000():
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
    message_senddm_response = requests.post(f"{config.url}message/senddm/v1",json={'token': user_1['token'], 'dm_id': dm_id, 'message': equal_1000_characters})
    assert message_senddm_response.status_code == SUCCESS_CODE
    messages_senddm_data = message_senddm_response.json()
    assert messages_senddm_data['message_id'] == 1

#Run successfully less1000_over1_characters
def test_message_senddm_message_less_1000_over_1():
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
    assert messages_senddm_data['message_id'] == 1


#Run successfully less1000_over1_characters
def test_message_senddm_2_message_less_1000_over_1():
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
    message_senddm_response_1 = requests.post(f"{config.url}message/senddm/v1",json={'token': user_1['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response_1.status_code == SUCCESS_CODE
    messages_senddm_data_1 = message_senddm_response_1.json()
    assert messages_senddm_data_1['message_id'] == 1

    #send message to dm
    message_senddm_response_2 = requests.post(f"{config.url}message/senddm/v1",json={'token': user_2['token'], 'dm_id': dm_id, 'message': less_1000_over_1_characters})
    assert message_senddm_response_2.status_code == SUCCESS_CODE
    messages_senddm_data_2 = message_senddm_response_2.json()
    assert messages_senddm_data_2['message_id'] == 2