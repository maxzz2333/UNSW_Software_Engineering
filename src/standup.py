import time
import datetime
import threading
from src.message import *
from src.error import InputError, AccessError
from src.data_store import data_store
from src.other import *
from src.helpers import decode_jwt

def standup_start_v1(token, channel_id, length):
    ''' Start a standup period

    Arguments:
    <token> (string)    - auth_user
    <channel_id> (integer)    - Existing channel
    <length> (integer)    - time of the standup period

    Exceptions:
    InputError when any of:
 
        channel_id does not refer to a valid channel
        length is a negative integer
        an active standup is currently running in the channel
      
      AccessError when:
      
        channel_id is valid and the authorised user is not a member of the channel
        
    Return Value:
    time_finish
    '''
    store = data_store.get()
    # Check if the token is valid
    if not check_token(token):
        raise AccessError("Given token is invalid")
    # Check if the user is valid
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

    # Check if the auth user is in the channel
    if auth_user_id not in channel['all_members']:
        raise AccessError("auth_user is not a member of the channel.") 
    # Check length
    if length < 0:
        raise InputError("Input length is negative.")

    # Check if an active standup is currently running
    if channel['standup']['is_active'] == True:
        raise InputError("An active standup is currently running in this channel.")

    # Start a standup
    channel['standup']['is_active'] = True    
    
    # Get the time finished
    dtime = datetime.datetime.now()
    time_created = int(time.mktime(dtime.timetuple()))
    channel['standup']['time_finished'] = time_created + length

    # send the standup queue
    t = threading.Timer(length, standup_end, [token, channel_id])
    t.start()
    return {"time_finish": channel['standup']['time_finished']}

def standup_end(token, channel_id):
    store = data_store.get()
    for channel in store['channels']:
        if channel_id == channel['id']:
            if channel['standup']['message'] != "":
                channel['standup']['message'] = channel['standup']['message'].strip('\n')
                message_send_v1(token, channel_id, channel['standup']['message'], enable_tagged=False)
            channel['standup']['is_active'] = False
            channel['standup']['time_finish'] = None
            channel['standup']['message'] = ""
            break
    
    
def standup_send_v1(token, channel_id, message):
    ''' Start a standup period

    Arguments:
    <token> (string)    - auth_user
    <channel_id> (integer)    - Existing channel
    <message> (string)    - message

    Exceptions:
    InputError when any of:
      
        channel_id does not refer to a valid channel
        length of message is over 1000 characters
        an active standup is not currently running in the channel
      
    AccessError when:
      
        channel_id is valid and the authorised user is not a member of the channel
    Return Value:
    {}
    '''  
    store = data_store.get()
    # Check if the token is valid
    if not check_token(token):
        raise AccessError("Given token is invalid")
    # Check if the user is valid
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

    # Check if the auth user is in the channel
    if auth_user_id not in channel['all_members']:
        raise AccessError("auth_user is not a member of the channel.") 
    
    # Check the length message
    if len(message) < 1 or len(message) > 1000 :
        raise InputError('length of message error')

    # Check if an active standup is running
    if channel['standup']['is_active'] == False:
        raise InputError('an active standup is not currently running in the channel')

    # Send a message to get buffered in the standup queue
    handle = get_handle_from_uid(auth_user_id)
    channel['standup']['message'] += f"{handle}: {message}\n"
    
    return{}

def standup_active_v1(token, channel_id):
    ''' Start a standup period

    Arguments:
    <token> (string)    - auth_user
    <channel_id> (integer)    - Existing channel

    Exceptions:
    InputError when:
      
        channel_id does not refer to a valid channel
      
    AccessError when:
      
        channel_id is valid and the authorised user is not a member of the channel
    Return Value:
    {is_active, time_finish}
    '''  
    store = data_store.get()
    # Check if the token is valid
    if not check_token(token):
        raise AccessError("Given token is invalid")
        
    # Check if the user is valid
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
        raise InputError("channel id is invalid.")  

    # Check if the auth user is in the channel
    if auth_user_id not in channel['all_members']:
        raise AccessError("auth_user is not a member of the channel.") 

    return {
        'is_active': channel['standup']['is_active'],
        'time_finish': channel['standup']['time_finished']
    }
