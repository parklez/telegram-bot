
from config import *

@bot.message_handler(commands=['talk'])
def reply_talk(message):
    cid = get_user_id(message)
    users_steps[cid] = 'talk'
    bot.send_message(cid, 'I am listening!')

@bot.message_handler(func=lambda message: get_user_step(get_user_id(message)) == 'talk')
def talk_to_chat(message):
    cid = get_user_id(message)
    
    if message.chat.id < 0:
        return

    if message.text == '/cancel':
        users_steps[cid] = ''
        bot.send_message(cid, 'Done!')
        
    else:
        bot.send_message(-183477300, message.text)