
import json
import os
import subprocess

from termcolor import cprint


class Cp_Problem:

    def fetch_problem(self, url=''):
        try:
            cprint(' ' * 17 + '...Parsing Problem...' + ' ' * 17, 'blue')
            if url == '':
                cprint('Enter the url : ', 'cyan', end='')
                url = input()
            cprint('-' * 55, 'magenta')

            cmd = 'oj-api get-problem ' + url
            cmd = list(cmd.split())

            cp = subprocess.run(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            problem = json.loads(cp.stdout)

            if problem['status'] == 'ok':
                # print('ok')
                try:
                    alphabet = problem['result']['context']['alphabet']
                except:
                    alphabet = ''
                problem_name = problem['result']['name']
                problem_name = alphabet + '-' + problem_name
                # print(problem_name)
                if not os.path.isdir(problem_name):
                    os.mkdir(problem_name)
                try:
                    result = f"\tFetched '{problem_name}' Successfully"
                    testcases = problem['result']['tests']

                    base = os.getcwd()
                    path = os.path.join(base, problem_name, "")

                    info = '{"name" : "$NAME" , "url" : "$URL" }'

                    info = info.replace('$NAME', problem_name)
                    info = info.replace('$URL', url)

                    with open(path + '.info', 'w') as f:
                        f.write(info)

                    if not os.path.isdir(path + "testcases"):
                        os.mkdir(path + "testcases")
                    path = os.path.join(path, 'testcases')
                    no = 1
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
                    cprint(result, 'green')

                except Exception as e:
                    print(e)

            else:
                result = "Wrong url."
                cprint(result, 'result')

            cprint('-' * 55, 'magenta')

        except Exception as e:
            print('-' * 55)
            # print(e)
            cprint("Sorry Can't Fetch.", 'red')
