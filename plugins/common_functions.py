'''
This module is meant to share common functions.

To make encoding work on linux, encoding="utf8"
was added as an argument when opening and saving files.
'''

from telebot import types

users_steps = dict()

def create_dict(file, dict_name=None):
    'Returns a new created file as dictionary.'
    if dict_name == None:
        dict_name = dict()
        
    with open(file, 'a') as f:
        f.write(str(dict_name))
    print(file, 'created!')
    
    return dict_name

def load_dict(file):
    'Returns a loaded file as a dictionary.'
    temp_dict = dict()
    try:
        with open(file, 'r', encoding='utf8') as f:
            temp_dict = eval(f.read())
        return temp_dict
    
    except FileNotFoundError:
        return create_dict(file)

def save_dict(file, dict_name):
    'Saves a dictionary into a file.'  
    try:
        with open(file, 'w', encoding='utf8') as f:
            f.write(str(dict_name))
            
    except FileNotFoundError:
        create_dict(file, dict_name)

def add_key_dict(file, dict_name, key, val):
    'Adds a key and a value to the memory and saves it into a file.'
    dict_name[key] = val
    save_dict(file, dict_name)

def remove_key_dict(file, dict_name, key):
    'Removes a key from the memory and saves it into a file.'
    try:
        del dict_name[key]
        save_dict(file, dict_name)
        
    except KeyError:
        print('Key:', key, 'not found!')
        return

def get_user_id(message):
    'Returns user\'s id, always.'
    return message.from_user.id
    '''
    if isinstance(message.chat, types.User):
        return message.chat.id
    else:
        return message.from_user.id
    '''

def get_user_step(user_id):
    'Returns user\'s current step.'
    if user_id not in users_steps:
        return ''
    else:
        return users_steps[user_id]

def get_file_extention(message):
    '''Returns the document's extention. It will fail if there is
    a dot before the actual extention type.
    Use telegram's mime_type instead.'''
    if message.content_type == 'document':
        name = message.document.file_name
        dot = name.find('.')
        extention = name[dot:len(name)]
        return extention
    else:
        return None

def heartbeat(telebot):
    'Retrieves information from telegram servers about the bot.'
    bot = telebot.get_me()
    print('------------------------')
    for key, val in sorted(bot.__dict__.items()):
        print(str(key) + ': ' + str(val))
    print('------------------------')
    
def make_dir(folder_name):
    'Creates a folder.'
    import os
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print('The folder', folder_name, 'has been created!')