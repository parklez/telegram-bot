from config import *

@bot.message_handler(commands=['viadao', 'nuncavi'])
def reply_viadao(message):
    bot.send_message(message.chat.id, 'Larga a mão de viadagem.')
    bot.send_sticker(message.chat.id, 'CAADAQADoQIAAj247wUHqp9mgEd9TwI')
    bot.send_voice(message.chat.id, 'AwADAQADBQADL3AAAUdHn5e1-VGGAwI')