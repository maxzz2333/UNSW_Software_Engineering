import time
import datetime 
import threading
from src.error import InputError
from src.error import AccessError
from src.data_store import data_store
from src.other import *
from src.error import AccessError
from src.error import InputError
from src.helpers import decode_jwt,generate_new_message_id
import re

from src.test_config import ACCESS_ERROR_CODE

def message_send_v1(token, channel_id, message, enable_tagged = True, m_id = None):
    '''
    Arguments:
    <token> (jwt)    
    <channel_id> (int)    
    <message> (str)  
    <enabled_tagged> (boolean)
    <m_id> (int):       The specified id

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
        InputError  - Occurs when message is less than 1 or over 1000 characters
        AccessError - Occurs channel_id is valid and the authorised user is not a member of the channel
        AccessError - Occurs when token is invalid
        AccessError - Occurs when authuser is invalid

    Return Value:
        Returns 'message_id': message_id
    '''
    if not check_token(token) :
        raise AccessError('token is invalid')

    #decode token
    token_data = decode_jwt(token)
    user_id =  token_data['u_id']
    session_id = token_data['session_id']
    if check_authorization(user_id , session_id) == False:
        raise AccessError('user is invalid')

    store = data_store.get()
    channels = store['channels']  # get channels  (type  list)
    check_channel_invalid = True

    for channel in channels : #(type  DIC)
        if channel_id == channel['id']:
            check_channel_invalid = False
            break
    
    if check_channel_invalid == True:
        raise InputError('channel_id is invalid')

    if user_id not in channel['all_members']:
        raise AccessError('user is not a member of the channel')

    if len(message) < 1 or len(message) > 1000 :
        raise InputError('length of message error')

    #cread unique message_id and get time
    if m_id is None:
        message_id = generate_new_message_id()
    else:
        message_id = m_id
    
    dtime = datetime.datetime.now()
    time_created = int(time.mktime(dtime.timetuple()))

    #Add messages_information to'Messages' and channel
    Messages = store['Messages'] #(type  DIC)
    messages_inf = {
        'message_id': message_id,
        'u_id': user_id,
        'message': message,
        'time_created': time_created,
        'reacts':[{'react_id' : 1, 'u_ids':[], 'is_this_user_reacted' : False}],
        'is_pinned': False
    }

    # Adding stats
    for user in store['users']:
        if user['u_id'] == user_id:
            curr_num_msgs = user['messages_sent'][-1]['num_messages_sent']
            user['messages_sent'].append({'num_messages_sent': curr_num_msgs + 1, 'time_stamp': time_created})

    workspace_stats = store['workspace_stats']
    num_curr_msgs = workspace_stats['messages_exist'][-1]['num_messages_exist']
    workspace_stats['messages_exist'].append({'num_messages_exist': num_curr_msgs + 1, 'time_stamp': time_created})

    Messages[message_id] = messages_inf
    channel['messages'].insert(0,message_id)  # get channels   (type  list)
    data_store.set(store)
    if enable_tagged:
        send_edit_messages_in_channel_or_DM_to_tagged_user_notification(user_id,channel,-1,message)
    
    return {
        'message_id': message_id
    }

def message_edit_v1(token, message_id, message):
    '''
    Arguments:
    <token> (jwt)    
    <message_id> (int)    
    <message> (str)  

    Exceptions:
        InputError  - Occurs when length of message is over 1000 characters
        InputError  - Occurs when message_id does not refer to a valid message within a channel/DM that the authorised user has joined
        AccessError - Occurs the message was not sent by the authorised user making this request and authorised user not has owner permissions in the channel/DM
        AccessError - Occurs when token is invalid
        AccessError - Occurs when authuser is invalid

    Return Value:
        Returns {}
    '''
    if not check_token(token):
        raise AccessError('token is invalid')

    #decode token
    token_data = decode_jwt(token)
    user_id =  token_data['u_id']
    session_id = token_data['session_id']

    store = data_store.get()
    channels = store['channels']    # get channels  (type  list)
    users_list = store['users']          # get users     (type  list)
    Messages = store['Messages']    # get Messages  (type  dic)
    dms = store['dm']               # get dms  (type  list)

    # Error
    if check_authorization(user_id , session_id) == False:
        raise AccessError('user is invalid')
    
    if message_id not in Messages:
       raise InputError('message is invalid') 

    if len(message) > 1000 :
        raise InputError('length of message error') 

    # check user permission and sent by the authorised user
    user_is_gobal_owner = False# check user is a global owner
    user_has_owner_permission_in_channel = False
    user_has_owner_permission_in_DM = False
    message_send_by_user = False

    messages_inf = Messages[message_id]
    if user_id == messages_inf['u_id']:
         message_send_by_user = True 

    for user in users_list:
        if user_id == user["u_id"]:
           edit_user = user

    if edit_user['permission_id'] == 1:
        user_is_gobal_owner = True
           
    for channel in channels:
        if message_id in channel['messages']:
            if user_id in channel['all_members'] and user_is_gobal_owner == True:
                user_has_owner_permission_in_channel = True

            if user_id in channel['owner_members']:
                user_has_owner_permission_in_channel = True

            if user_has_owner_permission_in_channel == False and message_send_by_user == False:
                raise AccessError('user can not edit')

            if (user_has_owner_permission_in_channel == True or message_send_by_user == True) and len(message) >= 1:
                messages_inf['message'] = message
                send_edit_messages_in_channel_or_DM_to_tagged_user_notification(user_id,channel,-1,message)

            if (user_has_owner_permission_in_channel == True or message_send_by_user == True) and len(message) == 0:
                del Messages[message_id]
                channel['messages'].remove(message_id)
                return {}
                
    
    for dm in dms:
        if message_id in dm['messages']:
            if user_id == dm['creator'] :
                user_has_owner_permission_in_DM = True

            if user_has_owner_permission_in_DM == False and message_send_by_user == False:
                raise AccessError('user can not edit')

            if (user_has_owner_permission_in_DM == True or message_send_by_user == True) and len(message) >= 1:
                messages_inf['message'] = message
                send_edit_messages_in_channel_or_DM_to_tagged_user_notification(user_id,-1,dm,message)

            if (user_has_owner_permission_in_channel == True or message_send_by_user == True) and len(message) == 0:
                del Messages[message_id]
                dm['messages'].remove(message_id)
            
    
    return {}

def message_remove_v1(token, message_id):
    '''
    Arguments:
    <token> (jwt)    
    <message_id> (int)     

    Exceptions:
        InputError  - message_id does not refer to a valid message within a channel/DM that the authorised user has joined
        AccessError - Occurs the message was not sent by the authorised user making this request and authorised user not has owner permissions in the channel/DM
        AccessError - Occurs when token is invalid
        AccessError - Occurs when authuser is invalid

    Return Value:
        Returns {}
    '''
    if not check_token(token):
        raise AccessError('token is invalid')

    #decode token
    token_data = decode_jwt(token)
    user_id =  token_data['u_id']
    session_id = token_data['session_id']

    store = data_store.get()
    channels = store['channels']    # get channels  (type  list)
    users_list = store['users']          # get users     (type  list)
    Messages = store['Messages']    # get Messages  (type  dic)
    dms = store['dm']               # get dms  (type  list)

    # Error
    if check_authorization(user_id , session_id) == False:
        raise AccessError('user is invalid')
    
    if message_id not in Messages:
       raise InputError('message is invalid') 

    # check user permission and sent by the authorised
    user_is_gobal_owner = False# check user is a global owner
    user_has_owner_permission_in_channel = False
    user_has_owner_permission_in_DM = False
    message_send_by_user = False

    messages_inf = Messages[message_id]
    if user_id == messages_inf['u_id']:
        message_send_by_user = True 

    for user in users_list:
        if user_id == user["u_id"]:
           remove_user = user

    if remove_user['permission_id'] == 1:
        user_is_gobal_owner = True
           
    for channel in channels:
        if message_id in channel['messages']:
            if user_id in channel['all_members'] and user_is_gobal_owner == True:
                user_has_owner_permission_in_channel = True

            if user_id in channel['owner_members']:
                user_has_owner_permission_in_channel = True

            if user_has_owner_permission_in_channel == False and message_send_by_user == False:
                raise AccessError('user can not remove')

            else:
                del Messages[message_id]
                channel['messages'].remove(message_id)
                
    for dm in dms:
        if message_id in dm['messages']:
            if user_id == dm['creator'] :
                user_has_owner_permission_in_DM = True

            if user_has_owner_permission_in_DM == False and message_send_by_user == False:
                raise AccessError('user can not edit')

            if (user_has_owner_permission_in_channel == True or message_send_by_user == True):
                del Messages[message_id]
                dm['messages'].remove(message_id)

    time_stamp = int(time.mktime(datetime.datetime.now().timetuple()))
    workspace_stats = store['workspace_stats']
    num_curr_msgs = workspace_stats['messages_exist'][-1]['num_messages_exist']
    workspace_stats['messages_exist'].append({'num_messages_exist': num_curr_msgs - 1, 'time_stamp': time_stamp})

    return {}

def message_senddm_v1(token, dm_id, message, enable_tagged=True, m_id=None):
    '''
    Arguments:
    <token> (jwt)    
    <dm_id> (int)
    <message> (str)     

    Exceptions:
        InputError  - dm_id does not refer to a valid DM
        InputError  - length of message is less than 1 or over 1000 characters
        AccessError - dm_id is valid and the authorised user is not a member of the DM
        AccessError - Occurs when token is invalid
        AccessError - Occurs when authuser is invalid

    Return Value:
        Returns {'message_id': message_id}
    '''
    if not check_token(token):
        raise AccessError('token is invalid')

    #decode token
    token_data = decode_jwt(token)
    user_id =  token_data['u_id']
    session_id = token_data['session_id']

    store = data_store.get()
    dms = store['dm']  # get dms  (type  list)
    check_dm_invalid = True

    # Error
    if check_authorization(user_id , session_id) == False:
        raise AccessError('user is invalid')

    for dm in dms : #(type  DIC)
        if dm_id == dm['dm_id']:
            check_dm_invalid = False
            break
    
    if check_dm_invalid == True:
        raise InputError('dm_id is invalid')

    if user_id not in dm['member']:
        raise AccessError('user is not a member of the dm')

    if len(message) < 1 or len(message) > 1000 :
        raise InputError('length of message error')

    # create unique message_id and get time
    if m_id is None:
        message_id = generate_new_message_id()
    else:
        message_id = m_id
    dtime = datetime.datetime.now()
    time_created = int(time.mktime(dtime.timetuple()))

    #Add messages_information to'Messages' and dm
    Messages = store['Messages'] #(type  DIC)
    messages_inf = {
        'message_id': message_id,
        'u_id': user_id,
        'message': message,
        'time_created': time_created,
        'reacts':[{'react_id' : 1, 'u_ids':[], 'is_this_user_reacted' : False}],
        'is_pinned': False
    }

    # Adding stats
    for user in store['users']:
        if user['u_id'] == user_id:
            curr_num_msgs = user['messages_sent'][-1]['num_messages_sent']
            user['messages_sent'].append({'num_messages_sent': curr_num_msgs + 1, 'time_stamp': time_created})

    workspace_stats = store['workspace_stats']
    num_curr_msgs = workspace_stats['messages_exist'][-1]['num_messages_exist']
    workspace_stats['messages_exist'].append({'num_messages_exist': num_curr_msgs + 1, 'time_stamp': time_created})

    Messages[message_id] = messages_inf
    dm['messages'].insert(0,message_id)  
    data_store.set(store)

    if enable_tagged:
        send_edit_messages_in_channel_or_DM_to_tagged_user_notification(user_id,-1,dm,message)
        
    return {
        'message_id': message_id
    }

def search_v1(token, query_str):
    '''
    Given a query string, search for messages in all of the channels/DMs
     that the user has joined that contain the query.
    
    Args:
        token (string): jwt of the authorized user
        query_str (string): search query

    Return:
        {"messages":[
            {
                'message_id': ,
                'u_id': ,
                'message': ,
                'time_created': ,
                'reacts': ,
                'is_pinned': 
            },
            {...}
        ]}

    Exception:
        InputError:     * length of query_str is less than 1 or over 1000 characters
        AccessError:    * token is invalid
    '''

    if not check_token(token):
        raise AccessError("channels_create: given token is invalid")
        
    auth_user_id, session_id = info_from_token(token)
    
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Given author id or session id does not exist")

    if len(query_str) == 0 or len(query_str) > 1000:
        raise InputError("Invalid query string")

    store = data_store.get()
    messages_list = store['Messages']
    channels = store['channels']
    dms = store['dm']

    results = []

    for channel in channels:
        if auth_user_id in channel['all_members']:
            for message_id in channel['messages']:
                message = messages_list[message_id]
                if query_str.lower() in message['message'].lower():
                    results.append(messages_list[message_id])
    
    for dm in dms:
        if auth_user_id in dm['member']:
            for message_id in dm['messages']:
                message = messages_list[message_id]
                if query_str.lower() in message['message'].lower():
                    results.append(messages_list[message_id])

    return {'messages': results}

def message_pin_v1(token, message_id):
    '''
    Arguments:
    <token> (jwt)    
    <message_id> (int)     

    Exceptions:
        InputError  - message_id does not refer to a valid message within a channel/DM that the authorised user has joined
        InputError  - the message is already pinned
        AccessError - Occurs the message_id refers to a valid message in a joined channel/DM and the authorised user does not have owner permissions in the channel/DM
        AccessError - Occurs when token is invalid
        AccessError - Occurs when authuser is invalid

    Return Value:
        Returns {}
    '''
    if not check_token(token):
        raise AccessError('token is invalid')

    #decode token
    token_data = decode_jwt(token)
    user_id =  token_data['u_id']
    session_id = token_data['session_id']

    store = data_store.get()
    channels = store['channels']    # get channels  (type  list)
    users_list = store['users']          # get users     (type  list)
    Messages = store['Messages']    # get Messages  (type  dic)
    dms = store['dm']               # get dms  (type  list)
    

    # Error
    if check_authorization(user_id , session_id) == False:
        raise AccessError('user is invalid')
    
    if message_id not in Messages:
        raise InputError('message is invalid')

    # check user permission 
    user_is_gobal_owner = False# check user is a global owner
    user_has_owner_permission_in_channel = False
    user_has_owner_permission_in_DM = False
    messages_inf = Messages[message_id] # get messages_info  (type  dic)

    for user in users_list:
        if user_id == user["u_id"]:
           pin_user = user

    if pin_user['permission_id'] == 1:
        user_is_gobal_owner = True
           
    for channel in channels:
        if message_id in channel['messages']:
            if user_id in channel['all_members'] and user_is_gobal_owner == True:
                user_has_owner_permission_in_channel = True

            if user_id in channel['owner_members']:
                user_has_owner_permission_in_channel = True

            if user_has_owner_permission_in_channel == False:
                raise AccessError('user can not pin')

            if messages_inf['is_pinned'] == True:
                raise InputError('message is already pinned')

            else:
                messages_inf['is_pinned'] = True
                return {}
                
    for dm in dms:
        if message_id in dm['messages']:
            if user_id == dm['creator'] :
                user_has_owner_permission_in_DM = True

            if user_has_owner_permission_in_DM == False:
                raise AccessError('user can not edit')

            if messages_inf['is_pinned'] == True:
                raise InputError('message is already pinned')

            else:
                messages_inf['is_pinned'] = True

    return {}



def message_unpin_v1(token, message_id):
    '''
    Arguments:
    <token> (jwt)    
    <message_id> (int)     

    Exceptions:
        InputError  - message_id does not refer to a valid message within a channel/DM that the authorised user has joined
        InputError  - the message is already unpinned
        AccessError - Occurs the message_id refers to a valid message in a joined channel/DM and the authorised user does not have owner permissions in the channel/DM
        AccessError - Occurs when token is invalid
        AccessError - Occurs when authuser is invalid

    Return Value:
        Returns {}
    '''
    if not check_token(token):
        raise AccessError('token is invalid')

    #decode token
    token_data = decode_jwt(token)
    user_id =  token_data['u_id']
    session_id = token_data['session_id']

    store = data_store.get()
    channels = store['channels']    # get channels  (type  list)
    users_list = store['users']          # get users     (type  list)
    Messages = store['Messages']    # get Messages  (type  dic)
    dms = store['dm']               # get dms  (type  list)
    

    # Error
    if check_authorization(user_id , session_id) == False:
        raise AccessError('user is invalid')
    
    if message_id not in Messages:
       raise InputError('message is invalid')

    # check user permission 
    user_is_gobal_owner = False# check user is a global owner
    user_has_owner_permission_in_channel = False
    user_has_owner_permission_in_DM = False
    messages_inf = Messages[message_id] # get messages_info  (type  dic)

    for user in users_list:
        if user_id == user["u_id"]:
           pin_user = user

    if pin_user['permission_id'] == 1:
        user_is_gobal_owner = True
           
    for channel in channels:
        if message_id in channel['messages']:
            if user_id in channel['all_members'] and user_is_gobal_owner == True:
                user_has_owner_permission_in_channel = True

            if user_id in channel['owner_members']:
                user_has_owner_permission_in_channel = True

            if user_has_owner_permission_in_channel == False:
                raise AccessError('user can not pin')

            if messages_inf['is_pinned'] == False:
                raise InputError('message is already unpinned')

            else:
                messages_inf['is_pinned'] = False
                return {}
                
    for dm in dms:
        if message_id in dm['messages']:
            if user_id == dm['creator'] :
                user_has_owner_permission_in_DM = True

            if user_has_owner_permission_in_DM == False:
                raise AccessError('user can not edit')

            if messages_inf['is_pinned'] == False:
                raise InputError('message is already unpinned')

            else:
                messages_inf['is_pinned'] = False

    return {}

def message_react_v1(token, message_id, react_id):
    '''
    Arguments:
    <token> (jwt)    
    <message_id> (int)
    <react_id> (int)     

    Exceptions:
        InputError  - message_id does not refer to a valid message within a channel/DM that the authorised user has joined
        InputError  - react_id is not a valid react ID
        InputError  - message already contains a react with ID react_id from the authorised user
        AccessError - Occurs when token is invalid
        AccessError - Occurs when authuser is invalid

    Return Value:
        Returns {}
    '''
    if not check_token(token):
        raise AccessError('token is invalid')

    #decode token
    token_data = decode_jwt(token)
    user_id =  token_data['u_id']
    session_id = token_data['session_id']
    store = data_store.get()
    channels = store['channels']    # get channels  (type  list)
    
    Messages = store['Messages']    # get Messages  (type  dic)
    dms = store['dm']               # get dms  (type  list)
    
    # Error
    if check_authorization(user_id , session_id) == False:
        raise AccessError('user is invalid')
    
    if message_id not in Messages:
        raise InputError('message is invalid')

    if react_id != 1:
        raise InputError('react_id is invalid')

    # check user permission 
    user_is_channel_member = False
    user_is_DM_member = False
    message_send_by_user = False
    messages_inf = Messages[message_id] # get messages_info  (type  dic)
    messages_ract_inf = messages_inf['reacts'] # get messages_ract_inf  (type  list)
    messages_ract_id1_inf = messages_ract_inf[0]

    # check user alread ract
    if user_id in messages_ract_id1_inf['u_ids']:
        raise InputError('user alread ract')

    if user_id == messages_inf['u_id']:
         message_send_by_user = True 

    #ract in channel
    for channel in channels:
        if message_id in channel['messages']:
            if user_id in channel['all_members']:
                user_is_channel_member = True

            if user_is_channel_member == False:
                raise InputError('user not join')

            if message_send_by_user == True:
                messages_ract_id1_inf['u_ids'].insert(0,user_id)
                messages_ract_id1_inf['is_this_user_reacted'] = True

            else :
                messages_ract_id1_inf['u_ids'].insert(0,user_id)
                react_messages_in_channel_or_DM_to_user_notification(user_id,messages_inf['u_id'],channel,-1)
                return {}

    #ract in DM
    for dm in dms:
        if message_id in dm['messages']:
            if user_id in dm['member'] :
                user_is_DM_member = True

            if user_is_DM_member == False:
                raise InputError('user not join')

            if message_send_by_user == True:
                messages_ract_id1_inf['u_ids'].insert(0,user_id)
                messages_ract_id1_inf['is_this_user_reacted'] = True

            else :
                messages_ract_id1_inf['u_ids'].insert(0,user_id)
                react_messages_in_channel_or_DM_to_user_notification(user_id,messages_inf['u_id'],-1,dm)        
    
    return {}


def message_unreact_v1(token, message_id, react_id):
    '''
    Arguments:
    <token> (jwt)    
    <message_id> (int)
    <react_id> (int)     

    Exceptions:
        InputError  - message_id does not refer to a valid message within a channel/DM that the authorised user has joined
        InputError  - react_id is not a valid react ID
        InputError  - the message does not contain a react with ID react_id from the authorised user
        AccessError - Occurs when token is invalid
        AccessError - Occurs when authuser is invalid

    Return Value:
        Returns {}
    '''
    if not check_token(token):
        raise AccessError('token is invalid')

    #decode token
    token_data = decode_jwt(token)
    user_id =  token_data['u_id']
    session_id = token_data['session_id']

    store = data_store.get()
    channels = store['channels']    # get channels  (type  list)
    Messages = store['Messages']    # get Messages  (type  dic)
    dms = store['dm']               # get dms  (type  list)
    
    # Error
    if check_authorization(user_id , session_id) == False:
        raise AccessError('user is invalid')
    
    if message_id not in Messages:
        raise InputError('message is invalid')

    if react_id != 1:
        raise InputError('react_id is invalid')

    # check user permission 
    user_is_channel_member = False
    user_is_DM_member = False
    message_send_by_user = False
    messages_inf = Messages[message_id] # get messages_info  (type  dic)
    messages_ract_inf = messages_inf['reacts'] # get messages_ract_inf  (type  list)
    messages_ract_id1_inf = messages_ract_inf[0]
    
    if user_id == messages_inf['u_id']:
         message_send_by_user = True

    #unract in channel
    for channel in channels:
        if message_id in channel['messages']:
            if user_id in channel['all_members']:
                user_is_channel_member = True

            if user_is_channel_member == False:
                raise InputError('user not join')

            if user_id not in messages_ract_id1_inf['u_ids']:
                raise InputError('user not ract')

            if message_send_by_user == True:
                messages_ract_id1_inf['u_ids'].remove(user_id)
                messages_ract_id1_inf['is_this_user_reacted'] = False        
            else:
                messages_ract_id1_inf['u_ids'].remove(user_id)
               

    #unract in DM
    for dm in dms:
        if message_id in dm['messages']:
            if user_id in dm['member'] :
                user_is_DM_member = True

            if user_is_DM_member == False:
                raise InputError('user not join')

            if user_id not in messages_ract_id1_inf['u_ids']:
                raise InputError('user not ract')
                
            if message_send_by_user == True:
                messages_ract_id1_inf['u_ids'].remove(user_id)
                messages_ract_id1_inf['is_this_user_reacted'] = False
            else:
                messages_ract_id1_inf['u_ids'].remove(user_id)       
    
    return {} 

def message_share_v1(token, og_message_id, message, channel_id, dm_id ):
    '''
    Share the message from the channel to a dm, or vice versa,
    the additional message is optional

    Args:
        token (string):         authorized user JWT
        og_message_id (int):    ID of the original message
        message (string):       the optional message in addition to the shared message
        channel_id (int):       ID of the channel that the message is being shared to,
                                is -1 if the message is to be shared to DM
        dm_id (int):            ID of the DM that the message is being shared to,
                                is -1 if the message is to be shared to channel

    Return:
        {"shared_message_id": }: message id of the new message 

    Exception:
        InputError:     * both channel_id and dm_id are invalid
                        * neither channel_id nor dm_id are -1
                        * og_message_id does not refer to a valid message within
                           a channel/DM that the authorised user has joined
                        * length of message is more than 1000 characters
        AccessError:    * the pair of channel_id and dm_id are valid but
                           the authorised user has not joined the channel or DM
                           they are trying to share the message to
                        * token is invalid
    '''

    if not channel_exist(channel_id) and not dm_exist(dm_id):
        raise InputError("Non exist channel_id or dm_id")
    elif channel_id != -1 and dm_id != -1:
        raise InputError("neither channel_id nor dm_id are -1")

    store = data_store.get()
    messages = store['Messages']
    channels = store['channels']
    dms = store['dm']

    if og_message_id not in messages.keys():
        raise InputError("original message does not exist")

    auth_user_id, session_id = info_from_token(token)

    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Given author id or session id does not exist")

    for channel in channels:
        if og_message_id in channel['messages']:
            if not is_channel_member(auth_user_id, channel['id']):
                raise InputError("Not a member of the original channel")
            break

    for dm in dms:
        if og_message_id in dm['messages']:
            if not is_dm_member(auth_user_id, dm['dm_id']):
                raise InputError("Not a member of the original dm")
            break

    new_message = f"{messages[og_message_id]['message']}\n{message}" if len(message) > 0 else f"{messages[og_message_id]['message']}"

    if channel_id == -1:
        shared_message_id = message_senddm_v1(token, dm_id, new_message)['message_id']
    else:
        shared_message_id = message_send_v1(token, channel_id, new_message)['message_id']


    return {'shared_message_id': shared_message_id }


def message_sendlater_v1(token, target_id, message, time_sent, to_channel=False, to_dm=False):
    '''Send a message from the authorised user to the channel specified by channel_id
         automatically at a specified time in the future.
    
    Args:
        token (str):            JWT of the authorized user
        target_id (int):        the channel/dm to which the message is sent
        message (str):          content
        time_sent (int):        UTC timestamp, indicate the time when the message is gonna be sent
        to_channel & to_dm:     specified where the message is sent

    Returns:
        message_id (int):   the new message id

    Exception:
        InputError:     * Channel_id does not refer to a valid channel
                        * Length of message is over 1000 characters
                        * Time_sent is a time in the past
        
        AccessError:    * Token is invalid
                        * channel_id is valid and the authorised user
                           is not a member of the channel they are trying to post to
    '''

    message_id = generate_new_message_id()

    if not check_token(token):
        raise AccessError("channels_create: given token is invalid")
        
    auth_user_id, session_id = info_from_token(token)
    
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Given author id or session id does not exist")

    if len(message) <= 0 or len(message) > 1000:
        raise InputError("Message's length not expected")

    if to_channel:    
        if not channel_exist(target_id):
            raise InputError("Target channel does not exist")
        if not is_channel_member(auth_user_id, target_id):
            raise AccessError("Authorized user is not a member of the channel")
    elif to_dm:
        if not dm_exist(target_id):
            raise InputError("Target DM does not exist")
        if not is_dm_member(auth_user_id, target_id):
            raise AccessError("Authorized user is not a member of the DM")

    dtime = datetime.datetime.now()    
    time_length = time_sent - int(time.mktime(dtime.timetuple()))
    if time_length <= 0:
        raise InputError("Time_sent is a time in the past")

    # send the message
    if to_channel:
        t = threading.Timer(time_length, message_send_v1, [token, target_id, message], {'enable_tagged': False, 'm_id': message_id})
    elif to_dm:
        t = threading.Timer(time_length, message_senddm_v1, [token, target_id, message], {'enable_tagged': False, 'm_id': message_id})
    t.start()
    
    return {'message_id': message_id}
