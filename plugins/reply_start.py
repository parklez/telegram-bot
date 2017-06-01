# Reply /start plugin.

from config import *

@bot.message_handler(commands=['start', 'help'])
def reply_start(message):
    cid = get_user_id(message)
		
    reply = '<b>Welcome cutie! ( ˘ ³˘)♥</b>'
    
    if help_commands:
        reply += '\n\nHere\'s all my plugins:\n'
    
    for key, val in sorted(help_commands.items()):
        reply += '/' + str(key) + ': ' + str(val) + '\n'
        
    bot.send_message(cid, reply, parse_mode='HTML')