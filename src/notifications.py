from src.error import InputError
from src.error import AccessError
from src.data_store import data_store
from src.other import *
from src.helpers import decode_jwt,generate_new_message_id



def notifications_get_v1(token):
    '''
    Arguments:
    <token> (jwt)     

    Exceptions:
        AccessError - Occurs when token is invalid
        AccessError - Occurs when authuser is invalid

    Return Value:
        Returns notifications    [{ channel_id, dm_id, notification_message }]
    '''
    if not check_token(token):
        raise AccessError('token is invalid')

    #decode token
    token_data = decode_jwt(token)
    user_id =  token_data['u_id']
    session_id = token_data['session_id']
    # Error
    if check_authorization(user_id , session_id) == False:
        raise AccessError('user is invalid')
    #get notifications
    store = data_store.get()
    notifications_info = store['Notifications']
    notifications_recent_info = []

    if user_id in notifications_info:
        notifications_all_info = notifications_info[user_id]
        notifications_recent_info = notifications_all_info[:20]
 
    return {'notifications' : notifications_recent_info }