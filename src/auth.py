from src.error import InputError, AccessError
from src.data_store import data_store
from re import fullmatch
from src.data_store import data_store
from src.other import check_authorization, check_token, info_from_token
from src.helpers import generate_jwt, generate_new_session_id, hash_pw
from src.other import is_removed_user
from src.config import *
import time, datetime
from random import randint
import smtplib, ssl

resetcode_list = {}

def auth_login_v1(email, password):
    '''
    Given a registered user's email and password,
    if they are matched, returns their `auth_user_id` value.

    Arguments:
        <email> (string)        - The email address of user
        <password> (string)     - password entered by the user
        ...

    Exceptions:
        InputError  - Occurs when:
                        * email entered does not belong to a user
                        * password is not correct

    Return Value:
        Returns {'auth_user_id': ___ } (dict) if the user successfully login
    '''

    store = data_store.get()

    # Paramter for error checking
    is_email_registered = False
    is_password_correct = False
    
    # Try to get the user_id from entered email and password
    id = 0
    for user in store['users']:
        if email == user["email"]:
            is_email_registered = True
            if is_removed_user(user):
                raise AccessError(description="You are a removed user")
            elif hash_pw(password) == user["password"]:
                is_password_correct = True
                id = user["u_id"]
                break
    
    # If the entered email does not belong to a user
    if is_email_registered == False:
        raise InputError("Email not registered")
    # If the password does not match the given email
    if is_email_registered == True and is_password_correct == False:
        raise InputError("Password not correct")
    
    current_session = generate_new_session_id()
    user['session_id'].append(current_session)

    return {
        'token': generate_jwt(id, current_session),
        'auth_user_id': id
    }

def auth_register_v1(email, password, name_first, name_last):
    '''
    Create a new account and store it in the database

    Arguments:
        <email> (string)            - user's email address for login
        <password> (string)         - user's password 
        <name_first> (string)       - user's first name
        <name_second> (string)      - user's last name

    Exceptions:
        InputError  - Occurs when:
                        * email's format is not correct
                        * email address is already being used 
                        * given password is less than 6 characters
                        * name_first is not between 1 and 50 characters inclusively
                        * name_last is not between 1 and 50 characters inclusively

    Return Value:
        Returns {'auth_user_id': ___ } (dict) if an account is successfully registered
    '''
    store = data_store.get()

    # Check email's format
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not fullmatch(regex, email):
        raise InputError("Invalid email")

    for user in store['users']:
        if email == user["email"] and user['permission_id'] != 0:
            raise InputError("Email already been registered")

    if len(password) < 6:
        raise InputError("Password should be at least 6 characters")

    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError("First name should between 1 and 50 characters inclusive")

    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError("Last name should between 1 and 50 characters inclusive")

    # Create an account
    # An user id and a handle_str is generated for the account
    new_name_first = ''.join(char for char in name_first.lower() if char.isalnum())
    new_name_last = ''.join(char for char in name_last.lower() if char.isalnum())
    handle = new_name_first + new_name_last 
    handle = handle[:20]
    handle_repeat = False
    exist_suffix = []

    for member in store['users']:
        if handle == member['handle_str'][:len(handle)] and not is_removed_user(member):
            handle_repeat = True
            current_suffix = member['handle_str'][len(handle):]
            if current_suffix != "":
                exist_suffix.append(int(current_suffix))
    if handle_repeat == True:
        if len(exist_suffix) != 0:
            for suffix in range(0, max(exist_suffix)+2):
                if suffix not in exist_suffix:
                    handle = handle + str(suffix)
        else:
            handle = handle + str(0)

    time_stamp = int(time.mktime(datetime.datetime.now().timetuple()))

    current_session = generate_new_session_id()
    if len(store['users']) == 0:
        permission = 1 # Global owner
        # initialising workspace_data
        workspace_data = store['workspace_stats']
        workspace_data['channels_exist'] = [{'num_channels_exist': 0, 'time_stamp': time_stamp}]
        workspace_data['dms_exist'] = [{'num_dms_exist': 0, 'time_stamp': time_stamp}]
        workspace_data['messages_exist'] = [{'num_messages_exist': 0, 'time_stamp': time_stamp}]
    else:
        permission = 2 # Member

    user = {
        'email': email,
        'u_id': len(store['users']) + 1,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle,
        'password': hash_pw(password),
        'session_id': [current_session],
        'permission_id': permission,
        'profile_img_url': url + 'static/default.jpg',
        'channels_joined': [{'num_channels_joined': 0, 'time_stamp': time_stamp}],
        'dms_joined': [{'num_dms_joined': 0, 'time_stamp': time_stamp}],
        'messages_sent': [{'num_messages_sent': 0, 'time_stamp': time_stamp}],
    }

    store['users'].append(user)

    return {
        'token': generate_jwt(user["u_id"], current_session),
        'auth_user_id': user["u_id"]
    }


def auth_logout_v1(token):
    '''
    Given an active token, invalidates the token to log the user out.

    Arguments:
        <token>         The user's token

    Exceptions:
        AccessError     Invalid token

    Return value:
        empty dict
    '''
    if not check_token(token):
        raise AccessError('token is invalid')

    auth_user_id, session_id = info_from_token(token)
    if not check_authorization(auth_user_id, session_id):
        raise AccessError("Invalid User")

    store = data_store.get()
    users = store['users']

    #find user information
    for user in users:
        if auth_user_id == user['u_id']:
            user['session_id'].remove(session_id)

    return {}

def auth_password_reset_request(email):
    '''
    Given an email address, if the user is a registered user, sends them an email containing a specific secret code.

    Arguments:
        <email>         The user's email

    Exceptions:
        none

    Return value:
        empty dict
    '''
    store = data_store.get()
    all_users = store["users"]

    # Seeing if it is a current user, if it is, send reset email and remove active sessions
    for user in all_users:
        if not is_removed_user(user) and user["email"] == email:
            user['session_id'] = []

            reset_code = ''.join(str(randint(0,9)) for x in range(6))
            global resetcode_list
            if reset_code not in resetcode_list:
                resetcode_list[reset_code] = user['u_id']
            else:
                # Duplicate codes, so keep generating new codes
                while reset_code in resetcode_list:
                    reset_code = ''.join(str(randint(0,9)) for x in range(6))
                resetcode_list[reset_code] = user['u_id']

            # Code copied from https://realpython.com/python-send-email/
            # Create a secure SSL context
            context = ssl.create_default_context()
            # Try to log in to server and send email
            try:
                server = smtplib.SMTP(smtp_server, smtpport)
                server.starttls(context=context) # Secure the connection
                server.login(sender_email, password)
                server.sendmail(sender_email, email, reset_code)
            except Exception as e:
                # Print any error messages to stdout
                print(e)
            finally:
                server.quit()

def auth_password_reset_reset(reset_code, new_password):
    '''
    Given a reset code for a user, set that user's new password to the password provided.

    Arguments:
        <reset_code>         The user's reset code
        <new_password>       The user's new password

    Exceptions:
        InputError           The password is too short, invalid reset code

    Return value:
        empty dict
    '''
    global resetcode_list
      
    if len(new_password) < 6:
        raise InputError("Password should be at least 6 characters")
    
    resetting_user_id = resetcode_list.pop(reset_code, None)
    if resetting_user_id == None:
        raise InputError("Not a valid reset code")
  
    all_users = data_store.get()['users']

    for user in all_users:
        if user['u_id'] == resetting_user_id:
            user['password'] = hash_pw(new_password)