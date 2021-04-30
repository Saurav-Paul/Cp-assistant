from termcolor import cprint

from tools.OJ.CP.add_test import CpAddTest
from tools.OJ.CP.bruteforce import CpBruteforce
from tools.OJ.CP.contest import CpContest
from tools.OJ.CP.extension import Cp_ext
from tools.OJ.CP.help import help_keys, args_help
from tools.OJ.CP.login import Cp_login
from tools.OJ.CP.problem import Cp_Problem
from tools.OJ.CP.setup import Cp_setup
from tools.OJ.CP.submit import Cp_Submit
from tools.OJ.CP.test import Cp_my_tester, Cp_Test
from tools.OJ.CP.url_manager import Cp_url_manager
from tools.run_program import if_run_type

cp_keys = ['-cp', '-Cp']


def cp_manager(msg):
    """
    It takes command and initialize operations according to the command
    :param msg:
    :return:
    """
    status = ''
    msg = msg.lower()
    ar = msg.split(sep=' ')

    if if_run_type(msg):
        pass

    elif 'dev' in ar or 'dev' in ar:
        obj = Cp_ext()
        obj.link()
    elif 'parse' in ar or 'listen' in ar:
        obj = Cp_ext()
        if 'link' in ar:
            obj.link()
        elif 'id' in ar:
            obj.id()
        elif 'contest' in ar:
            obj.parse_contest()
        else:
            obj.listen()
        status = '$SHELL'
    elif 'problem' in ar:
        obj = Cp_Problem()
        obj.fetch_problem()
    elif 'submit' in ar:
        msg = msg.replace('submit', '')
        msg = msg.replace(' ', '')
        obj = Cp_Submit()
        obj.find_files(msg)
    elif '-t' in ar or 'template' in ar:
        msg = msg.replace('-t', '')
        msg = msg.replace('template', '')
        msg = msg.split()

        if (len(msg)) == 0:
            msg = 'sol.cpp'
        else:
            msg = msg[0]

        obj = Cp_setup()
        obj.template(file_name=msg)

    elif 'contest' in ar:
        obj = CpContest()
        obj.parse_contest()

    elif 'login' in ar:
        obj = Cp_login()
        obj.login()
    elif 'add' in ar:
        obj = CpAddTest()
        obj.add_case()
    elif 'test-oj' in ar:
        msg = msg.replace('test -oj', '')
        msg = msg.replace(' ', '')
        obj = Cp_Test()
        obj.find_files(msg)
    elif 'test' in ar:
        msg = msg.replace('test', '')
        msg = msg.replace(' ', '')
        obj = Cp_my_tester()
        # obj.TLE = 1
        show = False
        debug_run = False
        if '-d' in ar:
            msg = msg.replace('-d', '')
            debug_run = True
        if '--show' in ar:
            msg = msg.replace('--show', '')
            show = True
        obj.find_files(msg, show, debug_run)
    elif 'setup' in ar:
        obj = Cp_setup()
        obj.setup()
    elif 'brute' in ar:
        obj = CpBruteforce()
        obj.run()
    elif 'gen' in ar:
        obj = Cp_setup()
        obj.gen_py()
    elif 'open' in ar:
        all = False
        if 'all' in ar:
            all = True

        obj = Cp_url_manager()
        obj.open(all)
    elif 'stand' in ar or 'standing' in ar:
        obj = Cp_url_manager()
        obj.stand()
    elif msg in help_keys:
        args_help()
    else:
        cprint('Arguments Error', 'red')
        args_help()

    return status


def if_cp_type(msg):
    """
    check whether given command is a cp type command
    :param msg:
    :return:
    """
    for key in cp_keys:
        if key in msg:
            msg = msg.replace(key, '')
            cp_manager(msg.lower())
            return True
    return False
