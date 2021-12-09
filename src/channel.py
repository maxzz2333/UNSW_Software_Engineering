from src.error import InputError, AccessError
from src.data_store import data_store
from src.other import *
from src.helpers import decode_jwt
import time, datetime

def channel_invite_v1(token, channel_id, u_id):
    ''' 
    Invite a new_user into a existing channel with given auth_user_id, 
    channel_id and u_id.

    Arguments:
    <token> (string)    - Inviter
    <channel_id> (integer)    - Existing channel
    <u_id> (integer)    - Invitee

    Exceptions:
    InputError  - when any of:      
        * channel_id does not refer to a valid channel.
        * u_id does not refer to a valid user.
        * u_id refers to a user who is already a member of the channel
    AccessError - when:
        * given auth_user_id or u_id does not exist    
        * channel_id is valid and the authorised user is not a member of 
        the channel.
        
    Return Value:
    Return a empty dictionary.
    '''
    store = data_store.get()

    if not check_token(token):
        raise AccessError("Given token is invalid")

    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Invalid User")

    # Check if the channel_id is valid.
    valid = False
    for channel in store['channels']:
        if channel_id == channel['id']:
            valid = True   
            break
    if valid == False: 
        raise InputError("id is invalid.")  
          
    if auth_user_id not in channel['all_members']:
        raise AccessError("auth_user is not a member of the channel.") 

    # Check whether the u_id exist
    if not check_authorization(u_id):
        raise InputError("Invalid u_id (Not an exist user)")

    for member in channel['all_members']:
        if member == u_id:
            raise InputError("u_id is already a member.")  
              
    channel['all_members'].append(u_id)
    # Adding stats
    time_stamp = int(time.mktime(datetime.datetime.now().timetuple()))
    for user in store['users']:
        if user['u_id'] == u_id:
            curr_num_channels = user['channels_joined'][-1]['num_channels_joined']
            user['channels_joined'].append({'num_channels_joined': curr_num_channels + 1, 'time_stamp': time_stamp})

    joined_user_in_channel_or_DM_notification(auth_user_id,u_id,channel,-1)
    return {}

def channel_details_v1(token, channel_id):
    '''
    Provide the basic detail of the given channel

    Arguments:
        auth_user_id (int)    - id of user who request the channel detail
        channel_id (int)      - id of the channel to be given detail

    Exceptions:
        InputError      - Occurs when channel_id doest not refer to a valid channel
        AccessError     - Occurs when:
                            * the given user_id doest not exist
                            * the channel_id is valid but the authorised user
                               is not a member of the channel

    Return Value:
        Returns a list which contain name, state (pulic/private),
         channel owner and member list of the given channel
    '''

    store = data_store.get()
    channels = store['channels']
    users = store['users']

    if not check_token(token):
        raise AccessError("Invalid token")
    
    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Invalid User")

    if not channel_exist(channel_id):
        raise InputError("Invalid channel id (Not an existing channel)")
        
    channel = channels[channel_id - 1]
    if not auth_user_id in channel['all_members']:
        raise AccessError("Invalid authority (Not a member of the channel)")

    info = {
        'name': channel['name'],
        'is_public': channel['is_public'],
        'owner_members': [],
        'all_members': [],
    }
    
    for uid in channel['owner_members']:
        info['owner_members'].append(get_user_info(users[uid - 1]))
    
    for uid in channel['all_members']:
        info['all_members'].append(get_user_info(users[uid - 1]))
    
    return info

def channel_messages_v2(token, channel_id, start):
    '''
    Arguments:
    <auth_user_id> (int)    
    <channel_id> (int)    
    <start> (int)    - <index of start>

    Exceptions:
        InputError  - Occurs when channel_id is invalid
        InputError  - Occurs when start is greater than the total number of messages
        AccessError - Occurs when nvalid auther id (Not an exist user)
        AccessError - Occurs when user is not a member of the channel

    Return Value:
        Returns ['end'] = -1 on <start is greater than the total number of messages>
        Returns['end'] = start+50 on <start is less than the total number of messages>
    '''
    if not check_token(token):
        raise AccessError('token is invalid')

    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Invalid User")

    store = data_store.get()
    channels = store['channels']  # get channels  (type  list)
    check_channel_invalid = True

    for channel in channels :
        if channel_id == channel['id']:
            check_channel_invalid = False
            break
    
    if check_channel_invalid == True:
        raise InputError('channel_id is invalid')

    if auth_user_id not in channel['all_members']:
        raise AccessError('user is not a member of the channel')

    messages_list = channel['messages'] # get messages_id list
    Messages = store['Messages'] #(type  DIC)
    messages_inf = {}
    messages_id_list = []
    messages_inf_list = []

    if start > len(messages_list):
        raise InputError("start is greater than the total number of messages")

    elif (start+50) > len(messages_list):
        messages_id_list = messages_list[start:]
        for messages_id in messages_id_list:
            messages_inf_list.append(Messages[messages_id])
        messages_inf['messages'] = messages_inf_list
        messages_inf['start'] = start
        messages_inf['end'] = -1

    else:
        messages_id_list = messages_list[start:(start+50)]
        for messages_id in messages_id_list:
            messages_inf_list.append(Messages[messages_id])
        messages_inf['messages'] = messages_inf_list
        messages_inf['start'] = start
        messages_inf['end'] = start+50                    
                    
    return messages_inf

def channel_join_v1(token, channel_id):
    ''' 
    Add a new user to this channel

    Arguments:
    <token> (string)    - The new user
    <channel_id> (integer)    - Existing channel

    Exceptions:
    InputError   -when any of:     
        * channel_id does not refer to a valid channel
        * the authorised user is already a member of the channel
    AccessError - when:     
        * the given user_id doest not exist
        * channel_id refers to a channel that is private and the authorised user is not already a channel member and is not a global owner
        
    Return Value:
    Return a empty dictionary.
    '''
    store = data_store.get()  

    if not check_token(token):
        raise AccessError("Given token is invalid")

    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Invalid User")
    
    # Check channel_id
    valid = False
    for channel in store['channels']:
        if channel_id == channel['id']:
            valid = True   
            break
    if valid == False: 
        raise InputError("id is invalid.")
        
    for member in channel['all_members']:
        if auth_user_id == member:
            raise InputError("User is already in this channel.")

    # Check Gloabl owner
    if channel['is_public'] == False:
        if not check_global_owner(auth_user_id):
            raise AccessError("This is a private channel.")
    
    channel['all_members'].append(auth_user_id)
    # Adding stats
    time_stamp = int(time.mktime(datetime.datetime.now().timetuple()))
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            curr_num_channels = user['channels_joined'][-1]['num_channels_joined']
            user['channels_joined'].append({'num_channels_joined': curr_num_channels + 1, 'time_stamp': time_stamp})

    return {}

def channel_leave_v1(token, channel_id):
    ''' 
    Remove a user of the channel

    Arguments:
    <token> (string)    - The user who is leaving
    <channel_id> (integer)    - Existing channel

    Exceptions:
    InputError   -when any of:     
        * channel_id does not refer to a valid channel
    AccessError - when:     
        * channel_id is valid and the authorised user is not a member of the channel
        
    Return Value:
    Return a empty dictionary.
    '''
    store = data_store.get()  

    if not check_token(token):
        raise AccessError("Given token is invalid")
    
    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Invalid User")

    # Check channel_id
    valid = False
    for channel in store['channels']:
        if channel_id == channel['id']:
            valid = True   
            break
    if valid == False: 
        raise InputError("channel_id is invalid.")
    
    flag = False
    for member in channel['all_members']:
        if auth_user_id == member:
            flag = True
            break
    
    if flag == False:
        raise AccessError("Channel_id is valid and the user is not a member of it.")

    for member in channel['owner_members']:
        if auth_user_id == member:
            channel['owner_members'].remove(member)
            break

    channel['all_members'].remove(auth_user_id)

    # Adding stats
    time_stamp = int(time.mktime(datetime.datetime.now().timetuple()))
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            curr_num_channels = user['channels_joined'][-1]['num_channels_joined']
            user['channels_joined'].append({'num_channels_joined': curr_num_channels - 1, 'time_stamp': time_stamp})

    return{}


def channel_addowner_v1(token, channel_id, u_id):
    ''' 
    Make user with user id u_id an owner of the channel.

    Arguments:
    <token> (string)    - Authorised user
    <channel_id> (integer)    - Existing channel
    <u_id> (integer)    - A member of the channel

    Exceptions:
    InputError when any of:
      
        channel_id does not refer to a valid channel
        u_id does not refer to a valid user
        u_id refers to a user who is not a member of the channel
        u_id refers to a user who is already an owner of the channel
      
      AccessError when:
      
        channel_id is valid and the authorised user does not have owner permissions in the channel
        
    Return Value:
    Return a empty dictionary.
    '''
    store = data_store.get()

    if not check_token(token):
        raise AccessError("Given token is invalid")

    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Invalid User")

    # Check if the channel_id is valid.
    valid = False
    for channel in store['channels']:
        if channel_id == channel['id']:
            valid = True   
            break
    if valid == False: 
        raise InputError("id is invalid.")  
          
    # Check if auth_user_id is a member of the channel
    if auth_user_id not in channel['all_members']:
        raise AccessError("Auth_user is not a member of the channel.")

    # Check if auth_user_id is a owner of the channel
    if auth_user_id not in channel['owner_members']:
        if not check_global_owner(auth_user_id):
            raise AccessError("Auth_user does not has owner permission.")   

    # Check whether the u_id exist
    if not check_authorization(u_id):
        raise InputError("Invalid u_id (Not an exist user)")

    # Check whether the u_id is a member of the channel
    if u_id not in channel['all_members']:
        raise InputError("u_id is not a member of the channel.")  

    # Check whether u_id is already a owner of the channel
    if u_id in channel['owner_members']:
        raise InputError('User is already a owner of the channel.')
     
    channel['owner_members'].append(u_id)
    return {}

def channel_removeowner_v1(token, channel_id, u_id):
    ''' 
    Remove user with user id u_id as an owner of the channel.

    Arguments:
    <token> (string)    - Authorised user
    <channel_id> (integer)    - Existing channel
    <u_id> (integer)    - A member of the channel

    Exceptions:
    InputError when any of:
      
        channel_id does not refer to a valid channel
        u_id does not refer to a valid user
        u_id refers to a user who is not an owner of the channel
        u_id refers to a user who is currently the only owner of the channel
      
      AccessError when:
      
        channel_id is valid and the authorised user does not have owner permissions in the channel
        
    Return Value:
    Return a empty dictionary.
    '''
    store = data_store.get()

    if not check_token(token):
        raise AccessError("Given token is invalid")

    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Invalid User")

    # Check if the channel_id is valid.
    valid = False
    for channel in store['channels']:
        if channel_id == channel['id']:
            valid = True   
            break
    if valid == False: 
        raise InputError("id is invalid.")  
          
    # Check if auth_user_id is a member of the channel
    if auth_user_id not in channel['all_members']:
        raise AccessError("Auth_user is not a member of the channel.")

    # Check if auth_user_id is a owner of the channel
    if auth_user_id not in channel['owner_members']:
        if not check_global_owner(auth_user_id):
            raise AccessError("Auth_user does not has owner permission.")   

    # Check whether the u_id exist
    if not check_authorization(u_id):
        raise InputError("Invalid u_id (Not an exist user)")

    # Check whether the u_id is a member of the channel
    if u_id not in channel['all_members']:
        raise InputError("u_id is not a member of the channel.")  

    # Check whether u_id is a owner of the channel
    if u_id not in channel['owner_members']:
        raise InputError('User is not a owner of the channel.')
    
    # Check if the user is the only owner.
    if len(channel['owner_members']) <= 1:
        raise InputError('This is the only owner of the channel(cannot be removed)')

    channel['owner_members'].remove(u_id)
    return {}