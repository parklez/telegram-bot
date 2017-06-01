#####################################

token = '364426062:AAFdiYGCEKhblIP2B8MVcIHwPcnxhOEfLlc'

admin_id = 329462464
admin_name = '@parklez'

#####################################

import telebot

from telebot import types

bot = telebot.TeleBot(token)

from plugins.common_functions import *

heartbeat(bot)

##################################
# Localization

make_dir('data/')
make_dir('files/')

admin_users_file = 'data/admins.txt'
#groups_ids_file = 'data/groups.txt'
#regular_users_file = 'data/users.txt'

# Here comes our amateur databases

help_commands = dict()
admin_commands = dict()

# Load dictionaries for every plugin

admin_users = load_dict(admin_users_file)
#groups_ids = load_dict(groups_ids_file)
#regular_users = load_dict(regular_users_file)

# Adding a first admin

add_key_dict(admin_users_file, admin_users, admin_id, admin_name)
