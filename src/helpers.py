'''Copied from COMP1531 lecture code 5.2'''
import hashlib
import jwt

SESSION_TRACKER = 0
MESSAGES_TRACKER= 0
DM_TRACKER = 0
SECRET = 'COMP1531'

def generate_new_session_id():
    """Generates a new sequential session ID

    Returns:
        number: The next session ID
    """
    global SESSION_TRACKER
    SESSION_TRACKER += 1
    return SESSION_TRACKER

def generate_new_message_id():
    """Generates a new sequential MESSAGES ID

    Returns:
        number: The next MESSAGES ID
    """
    global MESSAGES_TRACKER
    MESSAGES_TRACKER += 1
    return MESSAGES_TRACKER

def generate_new_dm_id():
    """Generates a new dm ID

    Returns:
        number: The next session ID
    """
    global DM_TRACKER
    DM_TRACKER += 1
    return DM_TRACKER

def reset_trackers():
    """Reset the global variables

    Returns:
        None
    """
    global SESSION_TRACKER
    global MESSAGES_TRACKER
    global DM_TRACKER
    SESSION_TRACKER = 0
    MESSAGES_TRACKER = 0
    DM_TRACKER = 0
    
def hash_pw(input_string):
    """Hashes the input string with sha256

    Args:
        input_string ([string]): The input string to hash

    Returns:
        string: The hexidigest of the encoded string
    """
    return hashlib.sha256(input_string.encode()).hexdigest()


def generate_jwt(u_id, session_id=None):
    """Generates a JWT using the global SECRET

    Args:
        u_id (int): The username
        session_id (int, optional): The session id, if none is provided will
                                         generate a new one. Defaults to None.

    Returns:
        string: A JWT encoded string
    """
    return jwt.encode({'u_id': u_id, 'session_id': session_id}, SECRET, algorithm='HS256')


def decode_jwt(encoded_jwt):
    """Decodes a JWT string into an object of the data

    Args:
        encoded_jwt ([string]): The encoded JWT as a string

    Returns:
        Object: An object storing the body of the JWT encoded string
    """
    return jwt.decode(encoded_jwt, SECRET, algorithms=['HS256'])