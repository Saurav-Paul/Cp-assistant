from settings._first_load_ import check_if_first_time
import sys, os
from termcolor import cprint
import random

from settings.config import if_config_type
from run.startup import start_up

start_up()


def print_start_name(name, weight, name_col, border_col):
    space_no = weight - len(name) - 2
    space_no = int(space_no / 2)
    cprint('-' * weight, border_col)
    cprint('|' + ' ' * space_no, border_col, end='')
    cprint(name, name_col, end='')
    cprint(' ' * space_no + '|', border_col)
    cprint('-' * weight, border_col)


def cp_start():
    try:

        color = ['magenta', 'yellow', 'cyan', 'blue']
        pt = 50
        name_col = random.choice(color)
        border_col = random.choice(color)
        print_start_name('ai-virtual-assistant', 50, name_col, border_col)

        pt = '-' * pt
        cprint(pt, border_col)
        from tools.OJ.cp import cp_manager

        lt = list(sys.argv)
        lt = lt[1:]
        msg = ''
        for w in lt:
            msg += w + ' '

        if if_config_type(msg):
            return

        status = cp_manager(msg.strip())

        cprint(pt, border_col)
        cprint(f' (^-^) -> Good luck sir.', 'green')
        cprint(pt, border_col)

        if status == '$SHELL':
            os.system('$SHELL')

    except:
        cprint("Can't open sir.", 'red')
