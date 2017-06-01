from config import *

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
        
            if m.chat.type == 'private':
                text = '{}[{}]: {}'.format(m.chat.first_name, m.chat.id, m.text)
                
            if m.chat.type == 'group':
                text = '{}[{}]@[{}]: {}'.format(m.from_user.first_name, m.from_user.id, m.chat.id, m.text)
        
            print(text.encode("utf-8", errors='ignore'))
            
bot.set_update_listener(listener)