import os
import subprocess
import time
from itertools import zip_longest
from threading import Timer
from termcolor import colored as clr, cprint
from settings.compiler import DEBUG
from system.platform import get_platform

from tools.OJ.CP.table import Table

cf_tool = True


class Cp_my_tester:
    TLE = 5
    RTE = False

    @staticmethod
    def empty_line_remover(text):
        # text = "".join([text for text in text.strip().splitlines(True) if text.strip("\r\n")])
        text = "".join([text for text in text.strip().splitlines(True) if text.strip()])
        return text

    @staticmethod
    def diff_print(name, value, color):
        cprint('  ' + name + ' :', 'yellow', attrs=['bold'])
        for x in value:
            x = '  ' + x
            cprint(x, color)

    @staticmethod
    def colorfull_diff_print(x, y):
        sz = len(x)
        cnt = 0
        cprint("  Output :", 'yellow', attrs=['bold'])
        for wx, wy in zip_longest(x, y, fillvalue=''):
            print('  ', end='')
            for o, e in zip_longest(wx, wy, fillvalue=''):
                if (o == e):
                    cprint(o, 'green', end='')
                else:
                    cprint(o, 'red', end='')
            print()
            cnt += 1
            if cnt >= sz:
                break

    def different(self, value, output, expected, case):
        x = output.split('\n')
        y = expected.split('\n')
        i = value.split('\n')
        pt = '  ' + '-' * 5 + 'Problem Found in ' + case + '-' * 5
        cprint(pt, 'yellow')
        self.diff_print('Input', i, 'cyan')
        self.colorfull_diff_print(x, y)

        obj = Table()
        obj.print(output, expected)

    def sub_process(self, cmd, value):

        t = time.time()

        tle = False
        kill = lambda process: process.kill()
        x = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        my_timer = Timer(self.TLE, kill, [x])

        try:
            my_timer.start()
            with x.stdin as f:
                f.write(value.encode())
                result = (x.communicate()[0]).decode('utf-8')

        except Exception as e:
            cprint(e, 'red')
            pass

        finally:
            my_timer.cancel()

        t = time.time() - t

        if (x.returncode != 0):
            self.RTE = True

        if (t >= self.TLE):
            tle = True

        return (result, tle)

    def sub_process_old(self, cmd, value):

        x = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        with x.stdin as f:
            f.write(value.encode())
            result = (x.communicate()[0]).decode('utf-8')
            # print(result)

        return (result, False)

    def make_testfolder(self):

        ok = False

        for file in os.listdir(os.getcwd()):
            try:
                if 'in' in file and '.txt' in file:
                    file_num = file.replace('in', '')
                    file_num = file_num.replace('.txt', '')
                    ans_file_name = 'ans' + file_num + '.txt'

                    if os.path.exists(ans_file_name):
                        ok = True

                        name = 'Sample-'
                        folder_name = 'testcases'
                        if os.path.isdir(folder_name):
                            pass
                        elif os.path.isdir('test'):
                            folder_name = 'test'
                        else:
                            os.mkdir(folder_name)

                        path_name = os.path.join(os.getcwd(), folder_name)
                        # print(path_name)
                        lt = os.listdir(path_name)
                        # print(lt)
                        ase = len(lt)
                        no = int(ase / 2) + 1

                        with open(file) as f:
                            x = f.read()
                        with open(ans_file_name) as f:
                            y = f.read()

                        fileName_in = name + str(no).zfill(2) + '.in'
                        fileName_out = name + str(no).zfill(2) + '.out'
                        print()

                        with open(os.path.join(path_name, fileName_in), 'w') as fin:
                            fin.write(x)
                        with open(os.path.join(path_name, fileName_out), 'w') as fout:
                            fout.write(y)
            except:
                pass

        return ok

    def test(self, file_name, show=False, debug_run=False):
        path = os.getcwd()
        # print(path, file_name)
        pt = '-' * 20 + file_name + '-' * 20
        cprint(pt, 'magenta')
        pt = (' ' * 17 + "...Testing...")
        cprint(pt, 'cyan')
        print()

        debug_flag = ''
        if debug_run:
            debug_flag = '-DPAUL -DLOCAL'

        case_folder = 'testcases'
        if os.path.isdir(case_folder):
            pass
        elif os.path.isdir('test'):
            case_folder = 'test'
        elif cf_tool:
            cf_test = self.make_testfolder()
            if cf_test == False:
                cprint("Test folder not available.", 'red', attrs=['bold'])
                return
        else:
            cprint("Test folder not available.", 'red', attrs=['bold'])
            return

        file_path = os.path.join(path, case_folder)
        lt = os.listdir(file_path)
        # print(lt)
        if len(lt) == 0:
            cprint('Not test file available.')
            return
        ext = file_name.rsplit(sep='.', maxsplit=1)
        type = ''
        if len(ext) > 1:
            if ext[1] == 'cpp':
                type = 'cpp'
            elif ext[1] == 'py':
                type = 'py'

        if type == 'cpp':
            sanitizer = "-Wshadow -Wconversion -g"

            cmd = f"g++ {debug_flag} {sanitizer} {file_name} -o test.out"
            t = time.time()
            okk = os.system(cmd)
            if okk != 0:
                cprint("Compilation Error, sir.", 'red')
                return
            t = time.time() - t
            t = '{:.4f}'.format(t)
            pt = (f' #  Compilation time {t} s')
            cprint(pt, 'cyan')
        passed = 0
        failed = 0
        test_files = []
        cases = 0
        for file in lt:
            ext = file.rsplit(sep='.', maxsplit=1)
            # print(f'file = {ext}')
            try:
                if ext[1] == 'in':
                    out = ext[0] + '.out'
                    if os.path.isfile(os.path.join(file_path, out)):
                        test_files.append((file, out))
                        cases += 1
                    else:
                        # print(f'{out} not found.')
                        pass
            except:
                pass
        if cases == 0:
            cprint(" # No testcase available.", 'red')
            return
        if cases == 1:
            cprint(" # 1 testcase found.", 'yellow')
        else:
            cprint(f' # {cases} testcases found', 'yellow')

        st = -1.0
        slowest = ''
        is_tle = False
        if get_platform() == 'Windows':
            run_cmd = 'test.out'
        else:
            run_cmd = './test.out'
        for f in test_files:
            file = f[0]
            out = f[1]
            self.RTE = False
            # print(f'testing {file} with {out}')
            ext = file.rsplit(sep='.', maxsplit=1)
            with open(os.path.join(file_path, file), 'r') as f:
                value = f.read()
            old_value = value
            value = self.empty_line_remover(value)
            t = time.time()
            print()
            cprint('  * ' + ext[0], 'yellow')
            if type == 'cpp':

                result = self.sub_process([run_cmd], value)
            elif type == 'py':
                result = self.sub_process(['python3', file_name], value)
            else:
                result = ('', False)
            tle = result[1]
            result = result[0]

            value = old_value  # returning the old value

            t = time.time() - t
            if t > st:
                st = t
                slowest = ext[0]
            # t = '{:.4}'.format(t)
            t = f'{t:.4f}'
            # print('code :\n',result)
            cprint('  * Time : ', 'cyan', end='')
            if tle:
                cprint('TLE', 'red')
                is_tle = True
            else:
                cprint(t, 'cyan')

            with open(os.path.join(file_path, out)) as f:
                ans = f.read()
            # print('Expected :\n',ans)
            if self.RTE:
                cprint('  * RTE', 'red')
                self.different(value, result, ans, ext[0])
                failed += 1

            elif result == ans:
                cprint('  * Passed', 'green')
                passed += 1
                if show == True:
                    self.different(value, result, ans, ext[0])
            else:
                cprint('  * WA', 'red')
                failed += 1
                if tle == False:
                    self.different(value, result, ans, ext[0])
                else:
                    is_tle = True

        print()
        st = f'{st:.4f}'
        pt = f' # Slowest : '
        cprint(pt, 'blue', end='')
        if is_tle:
            cprint('TLE', 'red', end='')
        else:
            cprint(st, 'blue', end='')
        cprint(' [' + slowest + ']', 'blue')

        pt = (f' # Status : {passed}/{passed + failed} (AC/Total)')
        cprint(pt, 'yellow')
        if failed == 0:
            cprint(" # Passed....", 'green')
        else:
            cprint(" # Failed....", 'red')

        if os.path.isfile('test.out'):
            os.remove('test.out')
        print()
        pt = '-' * 20 + '-' * len(file_name) + '-' * 20
        cprint(pt, 'magenta')

    def find_files(self, file_name='', show=False, debug_run=False):

        file_list = []
        # print(file_name)
        supported_ext = ['cpp', 'py']
        # print(os.getcwd)
        for file in os.listdir(os.getcwd()):
            try:
                ext = file.rsplit(sep='.', maxsplit=1)
                for i in supported_ext:
                    if ext[1] == i:
                        if file_name in file:
                            file_list.append(file)
            except:
                pass
        # print(file_list)
        sz = len(file_list)
        if sz == 1:
            self.test(file_list[0], show, debug_run)
        elif sz > 1:
            no = 1
            cprint("All the available files are given below.\n", 'yellow')
            for file in file_list:
                pt = (' ' * 4 + str(no) + ') ' + file)
                cprint(pt, 'blue')
                no += 1
            cprint(' ' * 4 + '0) Cancel operation', 'red')
            print()
            while True:
                cprint("Select the file index : ", 'cyan', end='')
                index = int(input())
                if index == 0:
                    cprint("Testing operation cancelled.", 'red')
                    break
                elif index < no:
                    self.test(file_list[index - 1], show, debug_run)
                    break
                else:
                    cprint("You have entered the wrong index.Please try again.", 'red')
        else:
            cprint("NO FILE FOUND :(", 'red')


class Cp_Test:

    def test_it(self, file_name):
        try:
            pt = '-' * 20 + file_name + '-' * 20
            cprint(pt, 'magenta')
            pt = (' ' * 17 + "...Testing...")
            print(clr(pt, 'blue'))
            cmd = "g++ " + file_name + " && oj t"
            # cmd = 'g++ '+file_name+' -o a.out'
            os.system(cmd)
            # cmd_all =[['g++',file_name,'-o','a.out'] , ['oj','t']]
            # cmd_all =[['oj','t']]
            # print(cmd)
            # for i in cmd_all:
            #     cp = subprocess.run(i, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # result = cp.stderr
            # result = result.replace('test failed',clr('test failed','red'))
            # result = result.replace('WA',clr('WA','red'))
            # result = result.replace('AC',clr('AC','green'))
            # print(result)
            pt = ('-' * 20 + '-' * len(file_name) + '-' * 20)
            cprint(pt, 'magenta')
        except Exception as e:
            if DEBUG:
                print(e)
            cprint("Got some error. :(", 'red')

    def find_files(self, file_name=''):

        file_list = []
        # print(file_name)
        supported_ext = ['cpp', 'py']
        # print(os.getcwd)
        for file in os.listdir(os.getcwd()):
            try:
                ext = file.rsplit(sep='.', maxsplit=1)
                for i in supported_ext:
                    if ext[1] == i:
                        if file_name in file:
                            file_list.append(file)
            except:
                pass
        # print(file_list)
        sz = len(file_list)
        if sz == 1:
            self.test_it(file_list[0])
        elif sz > 1:
            no = 1
            cprint("All the available files are given below.\n", 'yellow')
            for file in file_list:
                pt = (' ' * 4 + str(no) + ') ' + file)
                cprint(pt, 'blue')
                no += 1
            cprint(' ' * 4 + '0) Cancel operation', 'red')
            print()
            while True:
                cprint("Select the file index : ", 'cyan', end='')
                index = int(input())
                if index == 0:
                    cprint("Testing operation cancelled.", 'red')
                    break
                elif index < no:
                    self.test_it(file_list[index - 1])
                    break
                else:
                    cprint("You have entered the wrong index.Please try again.", 'red')
        else:
            cprint("NO FILE FOUND :(", 'red')
