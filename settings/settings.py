# Written By Saurav Paul
from tools.json_manager import JsonManager as JM
from tools.ConfigParser import ConfigParserManager as CM
from system.path import getpath
import os
from termcolor import cprint

all_sections = [
    'bot',
    'default',
    'interaction_setting',
    'cp',
    'template_path',
    'compiler',
    'developer',
    'start_time'

]

positive = ['yes', '1', 'true']

interaction_setting = {
    'voice_reply': True,
    'text_reply': True,
    'voice_read_voice_reply': False,
    'text_read': True,
}
bot = {
    'name': 'Jarvis',  # You can change bot name from here
    'gender': 'male',  # Whatever you want ;p
    'boss': 'Saurav Paul',  # you can put your name her ;p
    'voice_engine': 'robotic',  # you can change it to 'gTTS' for more natural voice (online)

}
conf_path = os.path.join(getpath(__file__), 'settings.conf')
# try:
#     obj = CM()
#     bot = obj.read(conf_path, section='bot')
#     print(bot)
#     print(type(bot))
# except Exception as e:
#     print('first_try', e)

DEBUG = True
LEARN = True

try:

    section = 'bot'
    obj = CM()
    bot = obj.read(conf_path, section=section)
    bot = dict(bot)
    section = 'interaction_setting'
    x = obj.read(conf_path, section=section)
    for i in interaction_setting:
        if x[i].lower() in positive:
            interaction_setting[i] = True
        else:
            interaction_setting[i] = False
    section = 'developer'
    x = obj.read(conf_path, section=section)

    if x['debug'].lower() in positive:
        DEBUG = True
    else:
        DEBUG = False

    if x['learn'].lower() in positive:
        LEARN = True
    else:
        LEARN = False


except Exception as e:
    cprint(e, 'red')
    print(conf_path)
    print(bot)
    cprint("Settings error.", 'red')

try:
    START_SCREEN_NAME = bot.get('name')  # Enter a string to make start screen banner
except Exception as e:
    print(e)


def update_bot(original_path):
    f = os.path.join(original_path, '/settings/bot.json')
    JM.json_write(bot)


def read_bot(original_path):
    global bot
    f = os.path.join(original_path, '/settings/bot.json')
    bot = JM.json_read(f)


def update_dev(xyz):
    global DEBUG

    if xyz['debug'].lower() in positive:
        DEBUG = True
    else:
        DEBUG = False


def get_bot():
    bot_obj = CM()
    bot_obj = dict(bot_obj.read(conf_path, section='bot'))
    print(bot_obj)
    return bot_obj
