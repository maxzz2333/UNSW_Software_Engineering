from src.error import InputError, AccessError
from src.data_store import data_store
from src.other import check_authorization, check_token, check_global_owner, info_from_token

def admin_user_remove_v1 (token, u_id):
    '''
        Arguments:
        <token> (jwt)    
        <u_id> (int)    

        Exceptions:
            InputError  -  u_id does not refer to a valid user
            InputError  -  u_id refers to a user who is the only global owner
            AccessError - the authorised user is not a global owner
            AccessError - Occurs when token is invalid
            AccessError - Occurs when authuser is invalid

        Return Value: return{}
    '''
    if not check_token(token):
        raise AccessError('token is invalid')

    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Invalid User")

    if check_global_owner(auth_user_id) == False:
        raise AccessError('authorised user is not a global owner') 

    store = data_store.get()
    channels = store['channels']    # get channels  (type  list)
    users_list = store['users']          # get users     (type  list)
    Messages = store['Messages']    # get Messages  (type  dic)
    dms = store['dm']               # get dms  (type  list)
    u_id_is_valid = False
    count_global_owner = 0

    # check u_id refers to a user is the only global owner and  valid
    for user in users_list:
        if user['permission_id'] == 1:
            count_global_owner += 1

        if u_id == user["u_id"]:
            u_id_is_valid = True
            user_info = user

    if u_id_is_valid == False:
        raise InputError('u_id is invalid')

    if count_global_owner == 1 and user_info['permission_id'] == 1:
        raise InputError('u_id refers to a user who is the only global owner')

    # remove user information from data_store
    user_info['name_first'] = 'Removed'
    user_info['name_last'] = 'user'
    user_info['password'] = ''
    user_info['session_id'] = []
    user_info['permission_id'] = 0
    user_info['channels_joined'] = []
    user_info['dms_joined'] = []
    user_info['messages_sent'] = []

    # replace their messages  'Removed user'
    for user_message in Messages.values():
        if u_id == user_message['u_id']:
           user_message['message'] = 'Removed user'

    # remove user from channel
    for channel in channels:
        if u_id in channel['all_members']:
            channel['all_members'].remove(u_id)
            if u_id in channel['owner_members']:
                channel['owner_members'].remove(u_id)

    # remove user from dm
    for dm in dms:
        if u_id in dm['member']:
            dm['member'].remove(u_id)
            if u_id == dm['creator']:
                dm['creator'] = None
        
    return{}

def admin_userpermission_change_v1(token, u_id, permission_id):
    ''' 
    Given a user by their user ID, set their permissions to new permissions described by permission_id.

    Arguments:
    <token> (string)    - auth_user
    <u_id> (integer)    - user
    <permission_id> (integer)    - 1 for global owner, 2 for user

    Exceptions:
    InputError when any of:
      
        u_id does not refer to a valid user
        u_id refers to a user who is the only global owner and they are being demoted to a user
        permission_id is invalid
      
      AccessError when:
      
        the authorised user is not a global owner
        
    Return Value:
    Return a empty dictionary.
    '''
    store = data_store.get()

    if not check_token(token):
        raise AccessError("Given token is invalid")

    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Invalid User")
    
    # Check if the auth user is a global owner
    if not check_global_owner(auth_user_id):
        raise AccessError("The auth user is not a global owner")

    # Check whether the u_id exist
    if not check_authorization(u_id):
        raise InputError("Invalid u_id (Not an exist user)")

    # Get the user information from stream
    for user in store['users']:
        if user['u_id'] == u_id:
            # Check if the permission id is valid
            # Change the permission id
            if permission_id == 1:
                if user['permission_id'] == 1:
                    raise InputError("User is already a global owner")
                else:
                    user['permission_id'] = 1
            elif permission_id == 2:
                if user['permission_id'] == 2:
                    raise InputError("User is already a user")
                else:
                    # Check if the user is the only global owner
                    only = True
                    for people in store['users']:
                        if people['permission_id'] == 1 and people['u_id'] != u_id:
                            only = False
                            break
                    if only == True:
                        raise InputError('This is the only global owner(cannot be demoted)')
                    else:
                        user['permission_id'] = 2
            else:
                raise InputError('Invalid permission_id')
                
    return {}




    
