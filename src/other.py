from src.data_store import data_store
from src.helpers import decode_jwt
import re

def clear_v1():
    '''
    Resets the internal data of the application to its initial state
    
    Arguments: None
    Exceptions: None
    Return Value: empty dict
    '''
    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    store['dm'] = []
    store['Messages'] = {}
    store['Notifications'] = {}
    store['workspace_stats'] = {}
    data_store.set(store)
    return {}

def check_token(token):
    '''Check whether the token is broken

    Args:
        token: the encoded JWT token
    
    Returns:
        Bool: True when the the token is valid,
                otherwise False    
    '''
    try:
        decode_jwt(token)
        return True
    except:
        return False

## Take an integer, check if the id exist
# the input id is an integer
def check_authorization(user_id, session_id = None):
    
    store = data_store.get()
    users_list = store['users']

    for user in users_list:
        if user_id == user["u_id"]:
            if session_id == None:
                return True
            elif session_id in user['session_id']:
                return True
    
    return False

## Take an user_id, check if he is a global owner
def check_global_owner(user_id):
    store = data_store.get()
    users_list = store['users']

    global_owner = False
    for user in users_list:
        if user_id == user['u_id']:
            if user['permission_id'] == 1:
                global_owner = True
    return global_owner

## Take an integer, check if the corresponding channel exist
# the input id is an integer
def channel_exist(channel_id):
    
    store = data_store.get()
    data_list = store['channels']

    for data in data_list:
        if channel_id == data["id"]:
            return True

    return False

def dm_exist(dm_id):
    '''Check whether the dm_id refer to a exist dm
    
    Args:
        dm_id (int):    id of the dm to be checked

    Return:
        Bool:   True when the dm is valid, 
                False when the dm is invalid
    '''
    store = data_store.get()
    dms = store['dm']

    for dm in dms:
        if dm_id == dm['dm_id']:
            return True
    
    return False

## Take a dictionary of individual user information
## Return a dict containing u_id, email, name_first, name_last and handle_str
def get_user_info(user):

    basic_info = {
        'u_id': user['u_id'],
        'email': user['email'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'handle_str': user['handle_str'],
        'profile_img_url': user['profile_img_url']
    }
    return basic_info

def info_from_token(token):
    user_info = decode_jwt(token)
    auth_user_id = user_info['u_id']
    session_id = user_info['session_id']

    return auth_user_id, session_id

def get_handle_from_uid(u_id):
    store = data_store.get()
    users_list = store['users']

    for user in users_list:
        if u_id == user['u_id']:
            return user['handle_str']

def get_uid_from_handle(handle):
    store = data_store.get()
    users_list = store['users']

    for user in users_list:
        if handle == user['handle_str']:
            return user['u_id']
    return False


def is_dm_creator(u_id, dm_id):
    '''Check whether the user is the creator of the DM
    
    Args:
        u_id (int):     id of the user to be checked
        dm_id (int):    id of the dm to be checked

    Return:
        Bool:   True when the user is creator of the given dm, 
                False when the user is not creator of the given dm
    '''
    store = data_store.get()
    dms = store['dm']

    for dm in dms:
        if dm_id == dm['dm_id'] and u_id == dm['creator']:
            return True
    
    return False

def is_removed_user(user):
    '''Check whether the given user is a removed user
    
    Args:
        user (dict):     dict of the user to be checked

    Return:
        True when the user is a removed user
        False when the user is not a removed user
    '''
    if user['permission_id'] == 0:
        return True
    else:
        return False

def is_dm_member(u_id, dm_id):
    '''Check whether the user is a member of the DM
    
    Args:
        u_id (int):     id of the user to be checked
        dm_id (int):    id of the dm to be checked

    Return:
        Bool:   True when the user is a member of the given dm, 
                False when the user is not a member of the given dm
    '''
    store = data_store.get()
    dms = store['dm']

    for dm in dms:
        if dm_id == dm['dm_id'] and u_id in dm['member']:
            return True
    
    return False

def is_channel_member(u_id, channel_id):
    '''Check whether the user is a member of the DM
    
    Args:
        u_id (int):     id of the user to be checked
        dm_id (int):    id of the dm to be checked

    Return:
        Bool:   True when the user is a member of the given dm, 
                False when the user is not a member of the given dm
    '''
    store = data_store.get()
    data_list = store['channels']

    for data in data_list:
        if channel_id == data['id'] and u_id in data['all_members']:
            return True
    
    return False

# if send messages in channel dm is -1, if send messages in dm, channel is -1
def send_edit_messages_in_channel_or_DM_to_tagged_user_notification(user_id,channel,dm,message):
    store = data_store.get()
    tagged_handles = re.findall(r'@[a-z0-9]+[a-z0-9]',message)
    if tagged_handles == []:
        return {}
    user_handle = get_handle_from_uid(user_id)
    new_tagged_handles = set(tagged_handles)#De-duplicate elements
    
    for tagged_handle in new_tagged_handles:
        tagged_user_handle = tagged_handle[1:]#Remove @
        tagged_user_id = get_uid_from_handle(tagged_user_handle)
        if tagged_user_id is False: #check user handle invalid
            continue
        if dm == -1:        
            if tagged_user_id not in channel['all_members']:
                continue
            else:
                Notifications_inf = {
                    'channel_id' : channel['id'],
                    'dm_id' : dm,
                    'notification_message' : f"{user_handle} tagged you in {channel['name']}: {message[:20]}"
                }
        else:
            if tagged_user_id not in dm['member']:
                continue
            else:
                Notifications_inf = {
                    'channel_id' : channel,
                    'dm_id' : dm['dm_id'],
                    'notification_message' : f"{user_handle} tagged you in {dm['name']}: {message[:20]}"
                }

        Notifications = store['Notifications']
        if tagged_user_id not in Notifications:
            Notifications[tagged_user_id] = [Notifications_inf]
        else:
            Notifications[tagged_user_id].insert(0,Notifications_inf)
    return{}


# if react messages in channel dm is -1, if react messages in dm, channel is -1
def react_messages_in_channel_or_DM_to_user_notification(user_id,reacted_user_id,channel,dm):
    store = data_store.get()
    user_handle = get_handle_from_uid(user_id)
    if dm == -1:
        Notifications_inf = {
            'channel_id' : channel['id'],
            'dm_id' : dm,
            'notification_message' : f"{user_handle} reacted to your message in {channel['name']}"
        }

    else:
        Notifications_inf = {
            'channel_id' : channel,
            'dm_id' : dm['dm_id'],
            'notification_message' : f"{user_handle} reacted to your message in {dm['name']}"
        }

    Notifications = store['Notifications']
    if reacted_user_id not in Notifications:
        Notifications[reacted_user_id] = [Notifications_inf]
    else:
        Notifications[reacted_user_id].insert(0,Notifications_inf)
    return{}

# if joined user in channel dm is -1, if joined user in dm, channel is -1
def joined_user_in_channel_or_DM_notification(user_id,joined_user_id,channel,dm):
    store = data_store.get()
    user_handle = get_handle_from_uid(user_id)
    if dm == -1:
        Notifications_inf = {
            'channel_id' : channel['id'],
            'dm_id' : dm,
            'notification_message' : f"{user_handle} added you to {channel['name']}"
        }

    else:
        Notifications_inf = {
            'channel_id' : channel,
            'dm_id' : dm['dm_id'],
            'notification_message' : f"{user_handle} added you to {dm['name']}"
        }

    Notifications = store['Notifications']
    if joined_user_id not in Notifications:
        Notifications[joined_user_id] = [Notifications_inf]
    else:
        Notifications[joined_user_id].insert(0,Notifications_inf)
    return{}