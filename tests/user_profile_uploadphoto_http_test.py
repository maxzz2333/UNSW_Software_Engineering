import requests
from src import config
from src.helpers import generate_jwt
from src.config import *

ACCESS_ERROR_CODE = 403
INPUT_ERROR_CODE = 400
SUCCESS_CODE = 200
USER_1 = {'email': "z5362100@ad.unsw.edu.au",
         'password': "password", 
         'name_first': "Glenn",
         'name_last': "Deng" }

USER_2 = {'email': "z5191576@ad.unsw.edu.au",
         'password': "password", 
         'name_first': "Harvey",
         'name_last': "Miao" }

PNG_URL = 'http://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-200.png'
JPG_URL = 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg' #159x200

'''
InputError when any of:
      
        img_url returns an HTTP status other than 200
        any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL
        x_end is less than x_start or y_end is less than y_start
        image uploaded is not a JPG
'''
def test_user_profile_uploadphoto_return_status_not_200():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    upload_response = requests.post(f"{config.url}user/profile/uploadphoto/v1",json={'token': user1_token, 'img_url': 'a', 'x_start': 0, 'y_start': 0, 'x_end': 60, 'y_end': 60})
    assert upload_response.status_code == INPUT_ERROR_CODE

def test_user_profile_uploadphoto_not_whitin_dimensions():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    upload_response = requests.post(f"{config.url}user/profile/uploadphoto/v1",json={'token': user1_token, 'img_url': JPG_URL, 'x_start': -1, 'y_start': 0, 'x_end': 60, 'y_end': 60})
    assert upload_response.status_code == INPUT_ERROR_CODE

def test_user_profile_uploadphoto_x_end_less_than_x_start():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    upload_response = requests.post(f"{config.url}user/profile/uploadphoto/v1",json={'token': user1_token, 'img_url': JPG_URL, 'x_start':70, 'y_start': 0, 'x_end': 60, 'y_end': 60})
    assert upload_response.status_code == INPUT_ERROR_CODE

def test_user_profile_uploadphoto_y_end_less_than_y_start():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    upload_response = requests.post(f"{config.url}user/profile/uploadphoto/v1",json={'token': user1_token, 'img_url': JPG_URL, 'x_start':0, 'y_start': 70, 'x_end': 60, 'y_end': 60})
    assert upload_response.status_code == INPUT_ERROR_CODE

def test_user_profile_uploadphoto_x_end_equal_x_start():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    upload_response = requests.post(f"{config.url}user/profile/uploadphoto/v1",json={'token': user1_token, 'img_url': JPG_URL, 'x_start':0, 'y_start': 0, 'x_end': 0, 'y_end': 60})
    assert upload_response.status_code == INPUT_ERROR_CODE

def test_user_profile_uploadphoto_img_is_not_jpg():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    upload_response = requests.post(f"{config.url}user/profile/uploadphoto/v1",json={'token': user1_token, 'img_url': PNG_URL, 'x_start':0, 'y_start': 0, 'x_end': 60, 'y_end': 60})
    assert upload_response.status_code == INPUT_ERROR_CODE

def test_user_profile_uploadphoto_invalid_token():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    upload_response = requests.post(f"{config.url}user/profile/uploadphoto/v1",json={'token': 'a', 'img_url': JPG_URL, 'x_start':0, 'y_start': 0, 'x_end': 60, 'y_end': 60})
    assert upload_response.status_code == ACCESS_ERROR_CODE

def test_user_profile_uploadphoto_invalid_u_id():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']

    upload_response = requests.post(f"{config.url}user/profile/uploadphoto/v1",json={'token': generate_jwt(user1_token, 2), 'img_url': JPG_URL, 'x_start':0, 'y_start': 0, 'x_end': 60, 'y_end': 60})
    assert upload_response.status_code == ACCESS_ERROR_CODE

def test_user_profile_uploadphoto_success():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    auth_response = requests.post(f"{config.url}auth/register/v2", json=USER_1)
    assert auth_response.status_code == SUCCESS_CODE
    user1_token = auth_response.json()['token']
    user1_id = auth_response.json()['auth_user_id']

    upload_response = requests.post(f"{config.url}user/profile/uploadphoto/v1",json={'token': user1_token, 'img_url': JPG_URL, 'x_start':0, 'y_start': 0, 'x_end': 120, 'y_end': 120})
    assert upload_response.status_code == SUCCESS_CODE
    
    photo_response = requests.get(f"{config.url}static/1.jpg")
    assert photo_response.status_code == SUCCESS_CODE

    user_response = requests.get(f"{config.url}user/profile/v1", params={'token': user1_token, 'u_id': user1_id})
    assert user_response.status_code == SUCCESS_CODE
    profile = user_response.json()

    assert profile == {
        'user': {
            'u_id': user1_id,
            'email': "z5362100@ad.unsw.edu.au", 
            'name_first': "Glenn",
            'name_last': "Deng",
            'handle_str': "glenndeng",
            'profile_img_url': url + 'static/1.jpg'
        }
    }