from src.error import InputError, AccessError
from src.data_store import data_store
from src.other import *
from src.helpers import decode_jwt, generate_new_dm_id
import time, datetime

def dm_create_v1(token, u_ids):
    '''Create a new direct message from the given user lists
    
    Args:
        token (string): token of the author
        u_ids ([int]): List of members' u_id

    Return:
        {dm_id}: id of the new dm

    Exception:
        InputError: when and u_id in the u_ids list does not refer to a valid user
        AccessError: token is invalid 
    '''

    if not check_token(token):
        raise AccessError("channels_create: given token is invalid")
        
    auth_user_id, session_id = info_from_token(token)
    
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Given author id or session id does not exist")

    for u_id in u_ids:
        if not check_authorization(u_id):
            raise InputError(f"the user id {u_id} does not refer to a valid user")

    store = data_store.get()
    dm_list = store['dm']

    new_id = generate_new_dm_id()
    member_list = u_ids
    member_list.append(auth_user_id)
    handle_list = []

    for id in member_list:
        handle_list.append(get_handle_from_uid(id))

    handle_list.sort()
    name = ", ".join(handle_list)

    new_dm = {
        'dm_id': new_id,
        'name': name,
        'creator': auth_user_id,
        'member': member_list,
        'messages': []
    }

    dm_list.append(new_dm)
    for u_id in u_ids:
        joined_user_in_channel_or_DM_notification(auth_user_id,u_id,-1,new_dm)
    
    # Adding stats
    time_stamp = int(time.mktime(datetime.datetime.now().timetuple()))
    for user in store['users']:
        if user['u_id'] in [auth_user_id] + u_ids:
            curr_num_dms = user['dms_joined'][-1]['num_dms_joined']
            user['dms_joined'].append({'num_dms_joined': curr_num_dms + 1, 'time_stamp': time_stamp})
    
    workspace_stats = store['workspace_stats']
    num_curr_dms = workspace_stats['dms_exist'][-1]['num_dms_exist']
    workspace_stats['dms_exist'].append({'num_dms_exist': num_curr_dms + 1, 'time_stamp': time_stamp})

    
    return {"dm_id": new_dm['dm_id']}

def dm_messages_v1(token, dm_id, start):
    '''
    Arguments:
    <auth_user_id> (int)    
    <dm_id> (int)    
    <start> (int)    - <index of start>

    Exceptions:
        InputError  - Occurs when dm_id is invalid
        InputError  - Occurs when start is greater than the total number of messages
        AccessError - Occurs when nvalid auther id (Not an exist user)
        AccessError - Occurs when user is not a member of the dm

    Return Value:
        Returns ['end'] = -1 on <start is greater than the total number of messages>
        Returns['end'] = start+50 on <start is less than the total number of messages>
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
        

    messages_list = dm['messages'] # get messages_id list
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

def dm_list_v1(token):
    '''Returns the list of DMs that the auth user is a member of.
    
    Args:
        token (string): encoded JWT token of the auth user

    Return:
        'dms': list of dictionary of the DMS, include the dm_id and dm's name

    Exception:
        AccessError: * when the token cannot be parsed
    '''
    
    if not check_token(token):
        raise AccessError("channels_create: given token is invalid")
        
    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Given author id or session id does not exist")

    store = data_store.get()
    dm_list = store['dm']

    dm_info = []
    for dm in dm_list:
        if auth_user_id in dm['member']:
            dm_info.append({'dm_id': dm['dm_id'], 'name': dm['name']})

    return {'dms':dm_info}

def dm_remove_v1(token, dm_id):
    '''Remove an existing DM, so all members are no longer in the DM. 
        This can only be done by the original creator of the DM.
    
    Args:
        token (string): the encoded JWT token of auth user
        dm_id: the DM id of which is going to be removed

    Return
        {}: Empty dict

    Exception:
        InputError:     * dm_id does not refer to a existing DM
        AccessError:    * The token cannot be parsed
                        * dm_id is valid but the authorised user
                            is not the original DM creator 
    '''
    if not check_token(token):
        raise AccessError("channels_create: given token is invalid")
        
    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Given author id or session id does not exist")

    if not dm_exist(dm_id):
        raise InputError("The given dm_id does not refer to a valid DM")
    elif not is_dm_creator(auth_user_id, dm_id):
        raise AccessError("Authorised user is not the creator of the given DM")
    
    store = data_store.get()
    dms = store['dm']

    num_msgs = 0

    member_list = []
    for dm in dms:
        if dm_id == dm['dm_id']:
            member_list = dm['member']
            num_msgs = len(dm['messages'])
            dms.remove(dm)

    # Adding stats
    time_stamp = int(time.mktime(datetime.datetime.now().timetuple()))
    for user in store['users']:
        if user['u_id'] in member_list:
            curr_num_dms = user['dms_joined'][-1]['num_dms_joined']
            user['dms_joined'].append({'num_dms_joined': curr_num_dms - 1, 'time_stamp': time_stamp})
    workspace_stats = store['workspace_stats']
    num_curr_dms = workspace_stats['dms_exist'][-1]['num_dms_exist']
    workspace_stats['dms_exist'].append({'num_dms_exist': num_curr_dms - 1, 'time_stamp': time_stamp})
    
    num_curr_msgs = workspace_stats['messages_exist'][-1]['num_messages_exist']
    workspace_stats['messages_exist'].append({'num_messages_exist': num_curr_msgs - num_msgs, 'time_stamp': time_stamp})

    return {}

def dm_leave_v1(token, dm_id):
    '''Given a dm_id, the authorised user is removed from the member list
    
    Args:
        token (string):     the encoded JWT of the authorised user
        dm_id (int):        id of the dm which the auth user want to leave

    Return
        {}:     Empty dict

    Exception:
        InputError:     * dm_id does not refer to a valid DM
        AccessError:    * Token cannot be parsed or session id is invalid
                        * dm_id is valid but the authorised user
                            is not a member of the DM
    '''
    if not check_token(token):
        raise AccessError("channels_create: given token is invalid")
        
    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Given author id or session id does not exist")

    if not dm_exist(dm_id):
        raise InputError("Given DM does not exist")
    
    if not is_dm_member(auth_user_id, dm_id):
        raise AccessError("Authorized user is not a member of the DM")
    
    store = data_store.get()
    dms = store['dm']

    for dm in dms:
        if dm_id == dm['dm_id']:
            if auth_user_id == dm['creator']:
                dm['creator'] == None
                dm['member'].remove(auth_user_id)
            else:
                dm['member'].remove(auth_user_id)

    # Adding stats
    time_stamp = int(time.mktime(datetime.datetime.now().timetuple()))
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            curr_num_dms = user['dms_joined'][-1]['num_dms_joined']
            user['dms_joined'].append({'num_dms_joined': curr_num_dms - 1, 'time_stamp': time_stamp})

    return {}

def dm_details_v1(token, dm_id):
    '''Given a DM with ID dm_id that the authorised user is a member of,
        provide basic details about the DM.

    Args:
        token (string):     encode JWT of the authorised user
        dm_id (int):        id of the DM

    Return:
        {'name', 'members'}:    name of the DM, list of members' detail
                                 including u_id, email, name_first, name_last
                                 and handle string

    Exception:
        InputError:     * dm_id does not refer to a valid DM
        AccessError:    * dm_id is valid but the authorised user
                            is not a member of the DM
                        * Token is invalid
    '''
    if not check_token(token):
        raise AccessError("channels_create: given token is invalid")
        
    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Given author id or session id does not exist")

    if not dm_exist(dm_id):
        raise InputError("Given DM does not exist")
    
    if not is_dm_member(auth_user_id, dm_id):
        raise AccessError("Authorized user is not a member of the DM")
    
    store = data_store.get()
    dms = store['dm']
    users = store['users']
    

    members_info = {
        'name': "",
        'members': []
    }

    for dm in dms:      
        if dm_id == dm['dm_id']:
            members_info['name'] = dm['name']
            for user in users:
                if user['u_id'] in dm['member']:
                    members_info['members'].append(get_user_info(user))
            break
    
    return members_info
