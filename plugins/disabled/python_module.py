# Python 3 version of the following bot:
# https://github.com/AndresCidoncha/Python-Bot

import sys
import io
import contextlib
import code

from config import *

nope_list = ['os.', 'sys.', '"os"', '"sys"', 'lambda', 'subprocess.','exit', '/etc/', 'input', 'open(', '.py', 'raise']
#'import'


# Create a console instance.

inter=code.InteractiveInterpreter()

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = io.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
    
@contextlib.contextmanager
def stderrIO(stderr=None):
    old = sys.stderr
    if stderr is None:
        stderr = io.StringIO()
    sys.stderr = stderr
    yield stderr
    sys.stderr = old      

def seccheck(text):
    for word in nope_list:
        if(word in text):
            return False
    return True
    
# Command Handlers

@bot.message_handler(commands=['python'])
def reply_python_mode(message):
    cid = get_user_id(message)

    users_steps[cid] = 'python'
    bot.send_message(message.chat.id, 'You\'re now in Python 3 console mode.\nTap /cancel to exit.\n<b>On groups, reply to my messages.</b>', parse_mode='HTML')

@bot.message_handler(func=lambda message: get_user_step(get_user_id(message)) == 'python')
def interpret(message):
    cid = get_user_id(message)
    
    text = message.text
    
    if text.startswith('/') and text != '/cancel' and text != '/cancel@parklezbot':
        return
    
    if text == '/cancel' or text == '/cancel@parklezbot':
        users_steps[cid] = ''
        bot.reply_to(message, 'Python console deactivated.')
        return
    
    if seccheck(text):
        with stdoutIO() as s:
            with stderrIO() as error:
                inter.runsource(text)
                text = s.getvalue()
                if text == '':
                    text = error.getvalue()
                    
                if text == '':
                    return
                    
                else:
                    if len(text) <= 4096:
                        bot.send_message(message.chat.id, text)
                        
                    else:
                        bot.send_message(message.chat.id, text[:4090] + '[...]')
        
    else:
        bot.reply_to(message, 'That\'s beyond what I can serve you.')
        
help_commands['python'] = 'Enters in a python 3 interactive console.'