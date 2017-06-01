# coding=UTF-8

from config import *

import importdir
importdir.do('plugins', globals())

# Pool for messages
bot.polling(none_stop=True)