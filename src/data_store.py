'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': [],
    'channels': [],
    'dm': [],  
    'Messages': {},
    'Notifications': {},
    'workspace_stats': {}
}

'''
Structure:
    initial_object = {
        'users': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
                'password': 'thisismypassword'
                'session_id': [1,2]
                'permission_id': 0 or 1 or 2 (1 for global owner, 2 for member, 0 for removed user),
                'profile_img_url': 'src/static/default.jpg',
                'channels_joined': [{'num_channels_joined': 0, 'time_stamp':1}],
                'dms_joined': [{'num_dms_joined': 0, 'time_stamp': 1}],
                'messages_sent': [{'num_messages_sent': 0, 'time_stamp': 1}],
            },
            {...}
        ],
        'channels': [
            {
                'id': 1,
                'name': "blah",
                'owner_members': [1],
                'all_members': [1, 2, 3, 4]
                "is_public": False
                'messages': [ 1,2,3,4 ]
                'standup': {
                    'is_active' : False or True,
                    'time_finished': ...,
                    'message': ...,
                    }                                      
            },
            {...}
        ],
        'dm' : [
        {
            'dm_id': 1
            'name': "haydensmith, haydensmith0"
            'creator': 1
            'member': [1, 2, 3]
            'messages': [1 ,2]
        },
        {...}
        ],
        'Messages': { 
            message_id_1 : { 
                        'message_id':1
                        'u_id': 1,
                        'message': 'Hello world',
                        'time_created': 1582426789
                        'reacts':[{'react_id' : 1 , 'u_ids':[u_id_1,u_id_2], 'is_this_user_reacted' : True or False}]
                        'is_pinned':True or False },
                        
            },
            message_id_2 : {...}
        }

        'Notifications' : {
            u_id_1 : [{'channel_id ' : 1, 'dm_id' : -1, 'notification_message' : str }],
            u_id_2 : [{'channel_id ' : 1, 'dm_id' : -1, 'notification_message' : str }]

        },
        'workspace_stats': {
            'channels_exist': [{'num_channels_exist': 0, 'time_stamp':1}],
            'dms_exist': [{'num_dms_exist': 0, 'time_stamp': 1}],
            'messages_exist': [{'num_messages_exist': 0, 'time_stamp': 1}],
        }
    }
'''
## YOU SHOULD MODIFY THIS OBJECT ABOVE

class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

print('Loading Datastore...')

global data_store
data_store = Datastore()

