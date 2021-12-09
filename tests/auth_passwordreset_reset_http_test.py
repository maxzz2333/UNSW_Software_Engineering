import requests
from src import config

ACCESS_ERROR_CODE = 403
INPUT_ERROR_CODE = 400
SUCCESS_CODE = 200

def test_passwordreset_reset_invalid_reset_code():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    reset_response = requests.post(f"{config.url}auth/passwordreset/reset/v1", json={'reset_code': 'abcdef', 'new_password': 'abcdef'})
    assert reset_response.status_code == INPUT_ERROR_CODE

def test_passwordreset_reset_invalid_password():
    clear_response = requests.delete(f"{config.url}clear/v1")
    assert clear_response.status_code == SUCCESS_CODE

    reset_response = requests.post(f"{config.url}auth/passwordreset/reset/v1", json={'reset_code': '111111', 'new_password': 'abcde'})
    assert reset_response.status_code == INPUT_ERROR_CODE