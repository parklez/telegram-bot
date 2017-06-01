# Thanks to https://github.com/JackRendor (he created this.)

import subprocess

from config import *

@bot.message_handler(commands=['shell'])
def shell_command(message):
    cid = get_user_id(message)
    if cid in admin_users:
        if message.text[7:] == '':
            markup = types.ForceReply(selective=False)
            msg = bot.send_message(message.chat.id, 'Send me your command:', reply_markup=markup)
            bot.register_next_step_handler(msg, execute_command)
        
        else:
            execute_command(message)
    
def execute_command(message):
    bot.send_message(message.chat.id, 'Executing...')
    if '/shell' in message.text:
        code = message.text[7:]
    else:
        code = message.text
        
    result_command = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE).stdout.read()
    
    if result_command.decode('utf-8') == '':
        bot.reply_to(message, 'Something went wrong!')
    else:
        bot.send_message(message.chat.id, result_command.decode('utf-8'))

admin_commands['shell'] = 'Runs a command on terminal.'