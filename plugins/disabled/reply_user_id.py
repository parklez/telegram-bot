# Reply user's ID.

from config import *

@bot.message_handler(commands=['me'])
def reply_user_id(message):
    bot.send_message(message.chat.id, 'Your personal ID: ' + str(message.from_user.id) + '\nChat\'s ID: ' + str(message.chat.id))

help_commands['me'] = 'Shows your ID.'
