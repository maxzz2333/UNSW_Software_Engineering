from src.data_store import data_store
from src.error import AccessError, InputError
from src.other import check_authorization, check_token, info_from_token
import time, datetime

def channels_list_v1(token):
    '''
    Takes in a user id and returns a list of all channels that the user is part of
    with the channel id and the channel name

    Arguments:
        <auth_user_id> (<int>)    - user's id

    Exceptions:
        InputError  - None
        AccessError - Occurs when the given user_id doest not exist

    Return Value:
        Returns a list of all channels that the user is part of
         with the channel id and the channel name

    '''
    if not check_token(token):
        raise AccessError('token is invalid')

    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Invalid User")

    store = data_store.get()
    all_channels = store["channels"]
    users_channels = []
    
    for channel in all_channels:
        if auth_user_id in channel["all_members"]:
            users_channels.append({"channel_id": channel["id"], "name": channel["name"]})
    
    return {"channels": users_channels}

def channels_listall_v1(token):
    '''
    Lists all the channels with their id and name if the user is registered.
    
    Arguments:
        <auth_user_id> (<int>)    - user's id

    Exceptions:
        InputError  - None
        AccessError - Occurs when the given user_id doest not exist

    Return Value:
        Returns a list of all channels with the channel id and the channel name

    '''
    if not check_token(token):
        raise AccessError('token is invalid')
    
    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Invalid User")

    store = data_store.get()
    all_channels = store["channels"]
    all_channel_info = []
    
    for channel in all_channels:
        all_channel_info.append({"channel_id": channel["id"], "name": channel["name"]})
    
    return {"channels": all_channel_info}


def channels_create_v1(token, name, is_public):
    '''
    Creates a new channel with the given name that is either a public or private channel.
    The user who created it automatically joins the channel.

    Arguments:
        auth_user_id (int)    - id of user who create the channel
        name (string)         - name of the channel
        is_public             - whether the channel is public or not

    Exceptions:
        InputError  - Occurs when invalid channel name is input
        AccessError - Occurs when the auth_user_id is not an existing user

    Return Value:
        Returns the channel id of the created channel (a list with key of 'channel_id')
    '''
    if not check_token(token):
        raise AccessError("channels_create: given token is invalid")
        
    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Invalid User")

    if len(name) < 1 or len(name) > 20:
        raise InputError("Invalid channel name (Unexpected length")

    store = data_store.get()
    channels = store['channels']

    new_channel = {
        'id': len(channels) + 1,
        'name': name,
        'owner_members':[auth_user_id],
        'all_members': [auth_user_id],
        'is_public': is_public,
        'messages':[],
        'standup': {
            'is_active' : False,
            'time_finished': None,
            'message': ""
        }
    }
    channels.append(new_channel)

    # Adding stats
    time_stamp = int(time.mktime(datetime.datetime.now().timetuple()))
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            curr_num_channels = user['channels_joined'][-1]['num_channels_joined']
            user['channels_joined'].append({'num_channels_joined': curr_num_channels + 1, 'time_stamp': time_stamp})
    
    workspace_stats = store['workspace_stats']
    num_curr_channels = workspace_stats['channels_exist'][-1]['num_channels_exist']
    workspace_stats['channels_exist'].append({'num_channels_exist': num_curr_channels + 1, 'time_stamp': time_stamp})


    return  {
        'channel_id' : new_channel['id']
    }
