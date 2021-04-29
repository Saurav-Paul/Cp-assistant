from tools.OJ.CP.add_test import Cp_add_test
from tools.OJ.CP.bruteforce import Cp_bruteforce
from tools.OJ.CP.contest import Cp_contest
from tools.OJ.CP.login import Cp_login
from tools.OJ.CP.problem import Cp_Problem
from tools.OJ.CP.setup import Cp_setup
from tools.OJ.CP.submit import Cp_Submit
from tools.OJ.CP.test import Cp_my_tester, Cp_Test
from tools.OJ.CP.table import Table

try:
    import os
    import webbrowser
    import subprocess
    import json
    from threading import Timer
    from termcolor import colored as clr, cprint
    import time
    from itertools import zip_longest
    from tqdm import tqdm
    import threading
    import socket
    import getpass
    from settings.compiler import competitive_companion_port, parse_problem_with_template
    from settings.compiler import template_path, coder_name, editor, DEBUG
    from system.get_time import digital_time
    from data.get_template import get_template
    from tools.run_program import if_run_type
except Exception as e:
    print(e)

cp_keys = ['-cp', '-Cp']

cf_tool = True

editor_file_path = []
editor_file_name = []


class Cp_ext:
    HOST = '127.0.0.1'
    PORT = competitive_companion_port

    def template(self, file_path, file_name='sol.cpp', open_editor=False):
        try:

            # print(open)
            obj_template = Cp_setup()
            obj_template.template(file_path, file_name, parsingMode=True, open_editor=open_editor)
            return
        except Exception as e:
            return

    def rectify(self, s):
        try:
            i = s.find('{')
            s = s[i:]
            return s
        except Exception as e:
            return ''

    def create(self, problem, cnt=0, link=False):
        # print(problem)
        try:
            problem = self.rectify(problem)
            dic = json.loads(problem)
            if link == True:
                dic = dic['result']

            # cprint(dic,'yellow')
            # return
            problem_name = dic['name']
            try:
                contest_name = dic['group']
            except:
                contest_name = 'NULL'
            url = dic['url']
            problem_timeLimit = 'NULL'
            problem_memoryLimit = 'NULL'
            try:
                problem_timeLimit = str(dic['timeLimit']) + ' ms'
                problem_memoryLimit = str(dic['memoryLimit']) + ' MB'
            except Exception as e:
                cprint(e, 'red')
                pass
            # cprint(f'{problem_name} : {contest_name} : {url} ','cyan')
            base = os.getcwd()
            base_name = os.path.basename(base)
            # cprint(f'{base_name}','cyan')
            contest_path = os.path.join(base, contest_name)
            # cprint(f'{contest_path}','yellow')
            # cprint(f'cnt = {cnt}','yellow')
            if base_name != contest_name and contest_name != 'NULL':
                if cnt == 0:
                    if not os.path.isdir(contest_name):
                        os.mkdir(contest_name)
                        cprint(f" Folder {contest_name} is created.", 'blue')
                        info = '{"contest_name" : "$CONTEST" , "url" : "$URL"}'
                        info = info.replace('$CONTEST', contest_name)
                        info = info.replace('$URL', url)
                        with open(os.path.join(contest_path, '.info'), 'w') as f:
                            f.write(info)
                    cprint(f" All the problems will be parsed into '{contest_name}' folder.\n", 'magenta')
                os.chdir(contest_path)

            # cprint(os.getcwd(),'red')
            if not os.path.isdir(problem_name):
                os.mkdir(problem_name)
                # print("problem created")

            info = '{"name" : "$NAME" , "url" : "$URL","timeLimit" : "$timeLimit" , "memoryLimit":"$memoryLimit"}'

            info = info.replace('$NAME', problem_name)
            info = info.replace('$URL', url)
            info = info.replace('$memoryLimit', problem_memoryLimit)
            info = info.replace('$timeLimit', problem_timeLimit)

            path = os.path.join(os.getcwd(), problem_name, "")
            # print(path)
            with open(path + '.info', 'w') as f:
                f.write(info)

            if parse_problem_with_template:
                open_editor = False
                if cnt == 0:
                    open_editor = True
                self.template(path, open_editor=open_editor)

            testcases = dic['tests']
            # print(testcases)
            # return
            no = 1
            if not os.path.isdir(path + "testcases"):
                os.mkdir(path + "testcases")
            path = os.path.join(path, 'testcases')

            for case in testcases:
                # print(case)
                fileName_in = 'Sample-' + str(no).zfill(2) + '.in'
                fileName_out = 'Sample-' + str(no).zfill(2) + '.out'
                # print(fileName_in)
                no += 1
                with open(os.path.join(path, fileName_in), 'w') as fin:
                    fin.write(case['input'])
                with open(os.path.join(path, fileName_out), 'w') as fout:
                    fout.write(case['output'])
            # cprint(result,'green')
            # print(info)
            cprint(f'  {problem_name} fetched successfully.', 'green')
            os.chdir(contest_path)

        except Exception as e:
            # cprint(e,'red')
            # cprint("Can't fetch.",'red')
            pass

    def listen(self):

        cprint(' ' * 17 + '...Parsing Problem...' + ' ' * 17, 'blue')
        print()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            cprint(" Listening (Click competitive companion extension)....", 'yellow')
            print()
            timeout = 1000
            cnt = 0
            ok = True
            while ok:
                try:
                    s.listen()
                    s.settimeout(timeout)
                    timeout = 2
                    conn, addr = s.accept()
                    with conn:
                        # cprint("Connected...",'green')
                        problem_json = ''
                        while True:
                            data = conn.recv(1024)
                            result = (data.decode('utf-8'))
                            # result = self.rectify(result)

                            if not data:
                                # cprint(problem_json,'cyan')
                                if problem_json == '':
                                    break
                                t = threading.Thread(target=self.create, args=(problem_json, cnt))
                                t.start()
                                cnt += 1
                                break
                            else:
                                problem_json += result
                                pass

                except:
                    ok = False

        print()
        t.join()
        cprint(f' # Total {cnt} problems is fetched.', 'blue')

        if cnt > 0 and editor != '$NONE':
            cli_editors = ['nvim', 'vim', 'nano']
            if editor not in cli_editors:
                os.system(editor + ' .')
            base = os.getcwd()
            for file_path, file_name in zip(editor_file_path, editor_file_name):
                os.chdir(file_path)
                os.system(editor + ' ' + file_name)
            os.chdir(base)

    def link(self):

        cprint(' ' * 17 + '...Parsing Problem...' + ' ' * 17, 'blue')
        print()
        cprint(" Enter the link of the problem : ", 'cyan', end='')
        url = input()
        print()
        cnt = 0
        ok = True
        while ok:
            try:

                cmd = 'oj-api get-problem --compatibility ' + url
                cmd = list(cmd.split())

                problem_json = subprocess.run(cmd, universal_newlines=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
                # print(problem_json.stdout)
                t = threading.Thread(target=self.create, args=(problem_json.stdout, cnt, True))
                t.start()
                ok = False
                cnt += 1
            except:
                ok = False

        print()
        t.join()
        print()
        cprint(f' # Total {cnt} problems is fetched.', 'blue')

    def id(self):

        cprint(' ' * 17 + '...Parsing Problem...' + ' ' * 17, 'blue')
        print()
        cprint(" Enter the codeforces contest id : ", 'cyan', end='')
        contest_id = input()
        cprint(" Enter the codeforces problems id : ", 'cyan', end='')
        problems = input()
        problems = problems.split(sep=' ')
        url = 'https://codeforces.com/contest/$CONTEST_ID/problem/$PROBLEM_ID'
        url = url.replace('$CONTEST_ID', contest_id)
        rem = url
        print()
        cnt = 0

        for prob in problems:
            try:
                url = rem.replace('$PROBLEM_ID', prob)
                cmd = 'oj-api get-problem --compatibility ' + url
                cmd = list(cmd.split())

                problem_json = subprocess.run(cmd, universal_newlines=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
                t = threading.Thread(target=self.create, args=(problem_json.stdout, cnt, True))
                t.start()
                cnt += 1
            except:
                cprint(" Invalid id : " + prob, 'red')

        print()
        t.join()
        print()
        cprint(f' # Total {cnt} problems is fetched.', 'blue')

    def parse_contest(self, url=''):
        try:

            cprint(' ' * 17 + '...Parsing Contest...' + ' ' * 17, 'blue')
            if url == '':
                cprint('Enter the url : ', 'cyan', end='')
                url = input()
            cprint('-' * 55, 'magenta')
            # os.system(cmd)
            t = time.time()
            cmd = 'oj-api get-contest ' + url
            cmd = list(cmd.split())

            cp = subprocess.run(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            contest = json.loads(cp.stdout)

            result = "\tFetched Contest info..."
            if contest['status'] == 'ok':
                cprint(result, 'green')
            else:
                cprint("Sorry contest can't be fetched. Sorry sir. :( ", 'red')
                return
            problems = contest['result']['problems']

            cnt = 0

            for prob in problems:
                try:

                    url = prob['url']
                    cmd = 'oj-api get-problem --compatibility ' + url
                    cmd = list(cmd.split())

                    problem_json = subprocess.run(cmd, universal_newlines=True, stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE)
                    t = threading.Thread(target=self.create, args=(problem_json.stdout, cnt, True))
                    t.start()
                    cnt += 1
                except:
                    cprint(" Invalid id : " + prob, 'red')

            print()
            t.join()
            print()
            cprint(f' # Total {cnt} problems is fetched.', 'blue')

        except Exception as e:
            cprint(e, 'red')


class Cp_url_manager:

    def cf_id_from_cwd(self):
        try:
            curr_path = os.getcwd()
            problem_id = curr_path.split(sep='/')
            problem_id = problem_id[-2] + ' ' + problem_id[-1]
            return problem_id
        except:
            return ''

    def check_cf_id(self, id):
        try:
            id = id.split(' ')
            if len(id) != 2:
                return False
            x = int(id[0])
            y = id[1]
            return True
        except:
            cprint('not cf id', 'red')
            return False

    def open_from_cwd(self):
        try:
            id = self.cf_id_from_cwd()

            if self.check_cf_id(id) == False:
                return False

            url = 'https://codeforces.com/contest/$CONTEST_ID/problem/$ALPHABET'
            id = id.split(sep=' ')
            url = url.replace('$CONTEST_ID', id[0])
            url = url.replace('$ALPHABET', id[1])

            webbrowser.open(url)
            cprint(' Check Browser.', 'yellow')
            return True

        except:
            return False

    def open(self, all=False):
        try:
            with open('.info', 'r') as f:
                info = f.read()
            info = json.loads(info)
            url = info['url']

            if all == True:
                if 'codeforces.com' in url:
                    lab = url.rsplit('/', maxsplit=1)
                    lab[-1] = ''
                    url = lab[0] + 's'
                elif 'atcoder.jp' in url:
                    lab = url.rsplit('/', maxsplit=1)
                    url = lab[0]

            webbrowser.open(url)
            cprint(' Check Browser.', 'yellow')

        except:
            if self.open_from_cwd() == False:
                cprint(" Can't find valid url.", 'red')

    def stand_from_cwd(self):
        try:
            id = self.cf_id_from_cwd()

            if self.check_cf_id(id) == False:
                return False

            stand_url = 'https://codeforces.com/contest/$CONTEST_ID/standings/friends/true'
            id = id.split(sep=' ')
            url = stand_url.replace('$CONTEST_ID', id[0])

            webbrowser.open(url)
            cprint(' Check Browser.', 'yellow')
            return True

        except Exception as e:
            print(e)
            return False

    def stand_open(self, url):

        if 'codeforces.com' in url:
            stand_url = 'https://codeforces.com/contest/$CONTEST_ID/standings/friends/true'
            id = url.split(sep='/')
            stand_url = stand_url.replace('$CONTEST_ID', id[-3])
            webbrowser.open(stand_url)
            cprint(' Check Browser.', 'yellow')

        elif 'atcoder.jp' in url:
            url = url.split(sep='/')
            url[-1] = ''
            url[-2] = 'standings'
            url = '/'.join(url)
            webbrowser.open(url)
            cprint(' Check Browser.', 'yellow')

        else:
            cprint(' Sorry sir, standing option has not implemented for this OJ.', 'red')

    def stand(self):

        try:
            with open('.info', 'r') as f:
                info = f.read()
            info = json.loads(info)
            url = info['url']

            self.stand_open(url)

        except:
            if self.stand_from_cwd() == False:
                cprint(" Can't find valid url.", 'red')


help_keys = ['-h', 'help']


def help():
    """All the available arguments are listed here"""
    pt = '-' * 18 + "cp command arguments" + '-' * 18
    cprint(pt, 'magenta')
    print()

    cprint('  -> parse : ', 'yellow', end='')
    cprint('To parse problem or contest via competitive companion extension', 'cyan')

    cprint('  -> listen : ', 'yellow', end='')
    cprint('To parse problem or contest via competitive companion extension', 'cyan')

    cprint('  -> test : ', 'yellow', end='')
    cprint('To test code against testcases', 'cyan')

    cprint('  -> add : ', 'yellow', end='')
    cprint('To add testcase', 'cyan')

    cprint('  -> brute : ', 'yellow', end='')
    cprint('To bruteforce solution', 'cyan')

    cprint('  -> gen : ', 'yellow', end='')
    cprint('To generate tescase generator', 'cyan')

    cprint('  -> setup : ', 'yellow', end='')
    cprint('To generate sol.cpp , brute.cpp and tescase generator', 'cyan')

    cprint('  -> -t "filename": ', 'yellow', end='')
    cprint('To generate "filename" from template', 'cyan')

    cprint('  -> login: ', 'yellow', end='')
    cprint('To login into online judge', 'cyan')

    cprint('  -> submit: ', 'yellow', end='')
    cprint('To submit problem', 'cyan')

    cprint('  -> problem : ', 'yellow', end='')
    cprint('To parse problem manually', 'cyan')

    cprint('  -> contest : ', 'yellow', end='')
    cprint('To parse contest manually', 'cyan')

    cprint('  -> open : ', 'yellow', end='')
    cprint('To open current problem in browser', 'cyan')

    cprint('  -> stand : ', 'yellow', end='')
    cprint('To open standing page in browser', 'cyan')

    print()
    cprint('-' * len(pt), 'magenta')


def cp_manager(msg):
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
        obj = Cp_contest()
        obj.parse_contest()

    elif 'login' in ar:
        obj = Cp_login()
        obj.login()
    elif 'add' in ar:
        obj = Cp_add_test()
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
        obj = Cp_bruteforce()
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
        help()
    else:
        cprint('Arguments Error', 'red')
        help()

    return status


def if_cp_type(msg):
    # print(msg)
    for key in cp_keys:
        if key in msg:
            msg = msg.replace(key, '')
            cp_manager(msg.lower())
            return True
    return False
