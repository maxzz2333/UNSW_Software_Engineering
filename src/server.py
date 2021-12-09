import signal
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from src.auth import *
from src.channel import *
from src.channels import *
from src.dm import *
from src.message import *
from src.admin import *
from src.user import *
from src.notifications import *
from src.users import *
from src import config
from src.data_store import data_store
import pickle
from src.other import clear_v1
from src.helpers import reset_trackers
from src.standup import *

try:
    data = pickle.load(open("datastore.p", "rb"))
    data_store.set(data)
except Exception:
	pass

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__, static_url_path="/static/")
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

def save_data():
    data = data_store.get()
    with open('datastore.p', 'wb') as FILE:
        pickle.dump(data, FILE)

@APP.route("/clear/v1", methods=['DELETE'])
def clear_all():
    clear_v1()
    save_data()
    reset_trackers()
    return {}

@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def reomve_user():
    u_data = request.get_json()
    admin_user_remove_v1(u_data['token'],u_data['u_id'])
    save_data()
    return {}

@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def change_userpermission():
    u_data = request.get_json()
    admin_userpermission_change_v1(u_data['token'], u_data['u_id'], u_data['permission_id'])
    save_data()
    return {}

@APP.route("/auth/register/v2", methods=['POST'])
def user_register():
    u_data = request.get_json()
    user_info = auth_register_v1(u_data['email'],u_data['password'],u_data['name_first'],u_data['name_last'])
    save_data()
    return dumps(user_info)

@APP.route("/channels/create/v2", methods=['POST'])
def create_new_channel():
    response = request.get_json()
    channel_id = channels_create_v1(response['token'],response['name'],response['is_public'])
    save_data()
    return dumps(channel_id)

@APP.route("/channel/details/v2", methods=['GET'])
def show_channel_detail():
    token = request.args.get('token')
    c_id = request.args.get('channel_id')
    c_detail = channel_details_v1(token, int(c_id))
    save_data()
    return dumps(c_detail)
    
@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    response = request.get_json()
    channel_join_v1(response['token'], response['channel_id'])
    save_data()
    return {}

@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    response = request.get_json()
    channel_leave_v1(response['token'], response['channel_id'])
    save_data()
    return {}

@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    response = request.get_json()
    channel_invite_v1(response['token'], response['channel_id'], response['u_id'])
    save_data()
    return {}

@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    response = request.get_json()
    channel_addowner_v1(response['token'], response['channel_id'], response['u_id'])
    save_data()
    return {}

@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner():
    response = request.get_json()
    channel_removeowner_v1(response['token'], response['channel_id'], response['u_id'])
    save_data()
    return {}

@APP.route("/auth/login/v2", methods=['POST'])
def user_login():
    response = request.get_json()
    user_identity = auth_login_v1(response['email'], response['password'])
    save_data()
    return dumps(user_identity)

@APP.route("/auth/logout/v1", methods=['POST'])
def user_logout():
    response = request.get_json()
    auth_logout_v1(response['token'])
    save_data()
    return {}

@APP.route("/channels/list/v2", methods=['GET'])
def user_channel_list():
    token = request.args.get('token')
    users_channels = channels_list_v1(token)
    save_data()
    return dumps(users_channels)

@APP.route("/channels/listall/v2", methods=['GET'])
def all_channel_list():
    token = request.args.get('token')
    all_channels = channels_listall_v1(token)
    save_data()
    return dumps(all_channels)

@APP.route("/message/send/v1", methods=['POST'])
def send_message():
    response = request.get_json()
    message_ID = message_send_v1(response['token'], response['channel_id'],response['message'])
    save_data()
    return dumps(message_ID)

@APP.route("/channel/messages/v2", methods=['GET'])
def get_message():
    token = request.args.get('token')
    cid = request.args.get('channel_id')
    start= request.args.get('start')
    messages_info = channel_messages_v2(token, int(cid),int(start))
    save_data()
    return dumps(messages_info)

@APP.route("/message/edit/v1", methods=['PUT'])
def edit_message():
    response = request.get_json()
    message_edit_v1(response['token'], response['message_id'],response['message'])
    save_data()
    return {}

@APP.route("/message/remove/v1", methods=['DELETE'])
def remove_message():
    response = request.get_json()
    message_remove_v1(response['token'], response['message_id'])
    save_data()
    return {}
    
@APP.route("/users/all/v1", methods=['GET'])
def get_all_users():
    token = request.args.get('token')
    user_list = users_all_v1(token)
    save_data()
    return dumps(user_list)

@APP.route("/user/profile/v1", methods=['GET'])
def get_user_profile():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    user_info = user_profile_info_v1(token, int(u_id))
    save_data()
    return dumps(user_info)

@APP.route("/user/profile/setname/v1", methods=['PUT'])
def set_users_name():
    response = request.get_json()
    token = response['token']
    name_first = response['name_first']
    name_last = response['name_last']
    user_profile_setname_v1(token, name_first, name_last)
    save_data()
    return {}

@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def set_users_email():
    response = request.get_json()
    token = response['token']
    email = response['email']
    user_profile_setemail_v1(token, email)
    save_data()
    return {}

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def set_users_handle():
    response = request.get_json()
    token = response['token']
    handle_str = response['handle_str']
    user_profile_sethandle_v1(token, handle_str)
    save_data()
    return {}

@APP.route("/dm/create/v1", methods=['POST'])
def create_new_dm():
    response = request.get_json()
    dm_id = dm_create_v1(response['token'],response['u_ids'])
    save_data()
    return dumps(dm_id)

@APP.route("/message/senddm/v1", methods=['POST'])
def senddm_message():
    response = request.get_json()
    message_ID = message_senddm_v1(response['token'], response['dm_id'],response['message'])
    save_data()
    return dumps(message_ID)

@APP.route("/dm/messages/v1", methods=['GET'])
def get_dmmessage():
    token = request.args.get('token')
    did = request.args.get('dm_id')
    start= request.args.get('start')
    messages_info = dm_messages_v1(token, int(did),int(start))
    save_data()
    return dumps(messages_info)
    
@APP.route("/dm/list/v1", methods=['GET'])
def list_dms():
    token = request.args.get('token')
    dms = dm_list_v1(token)
    save_data()
    return dumps(dms)

@APP.route("/dm/remove/v1", methods=['DELETE'])
def delete_given_dm():
    response = request.get_json()
    dm_remove_v1(response['token'],response['dm_id'])
    save_data()
    return {}

@APP.route("/dm/leave/v1", methods=['POST'])
def leave_dm():
    response = request.get_json()
    return_val = dm_leave_v1(response['token'],response['dm_id'])
    save_data()
    return dumps(return_val)

@APP.route("/dm/details/v1", methods=['GET'])
def get_dm_details():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    dm_details = dm_details_v1(token, int(dm_id))
    save_data()
    return dumps(dm_details)

@APP.route("/standup/start/v1", methods=['POST'])
def standup_start():
    response = request.get_json()
    time_finished = standup_start_v1(response['token'], response['channel_id'],response['length'])
    save_data()
    return dumps(time_finished)

@APP.route("/standup/send/v1", methods=['POST'])
def standup_send():
    response = request.get_json()
    standup_send_v1(response['token'], response['channel_id'],response['message'])
    save_data()
    return {}

@APP.route("/standup/active/v1", methods=['GET'])
def get_active():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    active_info = standup_active_v1(token, int(channel_id))
    save_data()
    return dumps(active_info)
@APP.route("/search/v1", methods=['GET'])
def search_messages():
    token = request.args.get('token')
    query_str  = request.args.get('query_str')
    result = search_v1(token, query_str)
    save_data()
    return dumps(result)

@APP.route("/message/pin/v1", methods=['POST'])
def message_pin():
    response = request.get_json()
    message_pin_v1(response['token'], response['message_id'])
    save_data()
    return {}

@APP.route("/message/unpin/v1", methods=['POST'])
def message_unpin():
    response = request.get_json()
    message_unpin_v1(response['token'], response['message_id'])
    save_data()
    return {}

@APP.route("/message/react/v1", methods=['POST'])
def message_react():
    response = request.get_json()
    message_react_v1(response['token'], response['message_id'],response['react_id'])
    save_data()
    return {}

@APP.route("/message/unreact/v1", methods=['POST'])
def message_unreact():
    response = request.get_json()
    message_unreact_v1(response['token'], response['message_id'],response['react_id'])
    save_data()
    return {}

@APP.route("/message/share/v1", methods=['POST'])
def share_message():
    response = request.get_json()
    shared_message_id = message_share_v1(response['token'], response['og_message_id'], response['message'], response['channel_id'], response['dm_id'])
    save_data()
    return dumps(shared_message_id)

@APP.route("/notifications/get/v1", methods=['GET'])
def get_notifications():
    token = request.args.get('token')
    notifications_inf = notifications_get_v1(token)
    save_data()
    return dumps(notifications_inf)

@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])
def upload_photo():
    response = request.get_json()
    user_profile_uploadphoto_v1(response['token'], response['img_url'], response['x_start'], response['y_start'], response['x_end'], response['y_end'])
    save_data()
    return {}

@APP.route("/static/<path:path>")
def send_js(path):
    return send_from_directory('', 'image/')

@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater_to_channel():
    response = request.get_json()
    new_message_id = message_sendlater_v1(response['token'], response['channel_id'], response['message'], response['time_sent'], to_channel=True)
    save_data()
    return dumps(new_message_id)

@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlater_to_dm():
    response = request.get_json()
    new_message_id = message_sendlater_v1(response['token'], response['dm_id'], response['message'], response['time_sent'], to_dm=True)
    save_data()
    return dumps(new_message_id)

@APP.route("/user/stats/v1", methods=['GET'])
def user_stats():
    token = request.args.get('token')
    user_stats_info = user_stats_v1(token)
    save_data()
    return dumps(user_stats_info)

@APP.route("/users/stats/v1", methods=['GET'])
def users_stats():
    token = request.args.get('token')
    users_stats_info = users_stats_v1(token)
    save_data()
    return dumps(users_stats_info)

@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def password_reset_request():
    response = request.get_json()
    auth_password_reset_request(response['email'])
    save_data()
    return {}

@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def password_reset_reset():
    response = request.get_json()
    auth_password_reset_reset(response['reset_code'], response['new_password'])
    save_data()
    return {}

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
