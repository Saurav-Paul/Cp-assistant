import os
import subprocess
import time
from itertools import zip_longest

from termcolor import cprint
from tqdm import tqdm

from tools.OJ.CP.table import Table


class Cp_bruteforce:

    def find_files(self, file_name=''):

        file_list = []
        # print(f'FIle name is {file_name}')
        supported_ext = ['cpp', 'py']
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
            return (file_list[0], True)
        elif sz > 1:
            xp = file_name
            if xp == '':
                xp = 'test'
            cprint(' ' * 17 + '...Choose ' + xp + ' file...' + '\n', 'blue')
            no = 1
            cprint("All the available files are given below.\n", 'yellow')
            for file in file_list:
                pt = (' ' * 4 + str(no) + ') ' + file)
                cprint(pt, 'blue')
                no += 1
            cprint(' ' * 4 + '0) Cancel operation', 'red')
            print()
            while True:
                cprint("Select the file number : ", 'cyan', end='')
                index = int(input())
                if index == 0:
                    cprint("Bruteforcing operation cancelled.", 'red')
                    return ('Cancelled', False)
                elif index < no:
                    return (file_list[index - 1], True)
                else:
                    cprint("You have entered the wrong index.Please try again.", 'red')
        else:
            cprint("NO FILE FOUND :(", 'red')
            return ('FILE NOT FOUND', False)

    def diff_print(self, name, value, color):
        cprint('  ' + name + ' :', 'yellow', attrs=['bold'])
        for x in value:
            x = '  ' + x
            cprint(x, color)

    def colorfull_diff_print(self, x, y):
        cprint("  Output :", 'yellow', attrs=['bold'])
        for wx, wy in zip_longest(x, y, fillvalue=''):
            print('  ', end='')
            for o, e in zip_longest(wx, wy, fillvalue=''):
                if (o == e):
                    cprint(o, 'green', end='')
                else:
                    cprint(o, 'red', end='')
            print()

    def different(self, value, output, expected):
        print()
        i = value.split('\n')
        pt = '  ' + '-' * 5 + 'Problem Found' + '-' * 5
        cprint(pt, 'yellow')
        print()

        self.diff_print('Input', i, 'cyan')

        obj = Table()
        obj.print(output, expected)
        return

    def sub_process(self, cmd, value, iput):

        x = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # print('here')
        with x.stdin as f:
            if iput:
                f.write(value.encode())
            result = (x.communicate()[0]).decode('utf-8')
            # print(result)

        return (result, False)

    def cmd_manager(self, file_name, value, ext, iput=True):
        pass
        if ext == 'py':
            cmd = ['python3', file_name]
        elif ext == 'cpp':
            ext = file_name.rsplit(sep='.', maxsplit=1)
            cmd = './' + ext[0] + '.out'
            cmd = [cmd]
        else:
            cprint('command manager failed.', 'red')
            return ''
        # print(cmd)
        return self.sub_process(cmd, value, iput)[0]

    def add_case(self, x, y, no=1, name='Genarated-'):
        """  function for adding testcases """
        try:

            test_folder = 'testcases'
            if os.path.isdir('testcases'):
                test_folder = 'testcases'
            elif os.path.isdir('test'):
                test_folder = 'test'
            else:
                os.mkdir('testcases')

            path_name = os.path.join(os.getcwd(), test_folder)
            # print(path_name)
            lt = os.listdir(path_name)
            # print(lt)
            ase = len(lt)
            no = int(ase / 2) + 1

            fileName_in = name + str(no).zfill(2) + '.in'
            fileName_out = name + str(no).zfill(2) + '.out'
            # print(fileName_in)
            no += 1
            with open(os.path.join(path_name, fileName_in), 'w') as fin:
                fin.write(x)
            with open(os.path.join(path_name, fileName_out), 'w') as fout:
                fout.write(y)

            cprint('Testcase added Sucessfully. :D', 'green', attrs=['bold'])

        except:
            cprint("Can't add testcase. :( ", 'red', attrs=['bold'])

    def remove_unnecessary(self, lt):
        for x in lt:
            try:
                os.remove(x)
            except:
                pass

    def run(self):
        pass

        need_to_removed = []

        brute_file = self.find_files('brute')
        # print(brute_file)
        if brute_file[1] == False:
            return
        # print(brute_file[0])
        gen_file = self.find_files('gen')
        # print(gen_file)
        # print(gen_file[1])
        if gen_file[1] == False:
            return
        test_file = self.find_files('')
        if test_file[1] == False:
            return

        test_file = test_file[0]
        brute_file = brute_file[0]
        gen_file = gen_file[0]
        # print(test_file)
        cprint('How many times do you want to stress? : ', 'cyan', end='')
        no = int(input())
        if no < 1:
            cprint('You want to bruteforce test less than 1 time? Seriously man? (-_-)', 'red')
            return
        # testing....
        print()
        brute_ext = brute_file.rsplit(sep='.', maxsplit=1)[1]
        gen_ext = gen_file.rsplit(sep='.', maxsplit=1)[1]
        test_ext = test_file.rsplit(sep='.', maxsplit=1)[1]
        # print(brute_ext,gen_ext,test_ext)
        if brute_ext == 'cpp':
            # print('cpp = ',brute_file)
            ext = brute_file.rsplit(sep='.', maxsplit=1)[0] + '.out'
            cmd = "g++ " + brute_file + " -o " + ext
            need_to_removed.append(ext)

            with tqdm(total=1.0, desc=brute_file + ' compiling', initial=.25) as pbar:
                exc_code = os.system(cmd)
                pbar.update(.75)
            print()
            if exc_code != 0:
                return
        if gen_ext == 'cpp':
            # print('cpp = ',gen_file)
            ext = gen_file.rsplit(sep='.', maxsplit=1)[0] + '.out'
            cmd = "g++ " + gen_file + " -o " + ext
            need_to_removed.append(ext)

            with tqdm(total=1.0, desc=gen_file + ' compiling', initial=.25) as pbar:
                exc_code = os.system(cmd)
                pbar.update(.75)
            print()
            if exc_code != 0:
                return

        if test_ext == 'cpp':
            # print('cpp = ',test_file)
            ext = test_file.rsplit(sep='.', maxsplit=1)[0] + '.out'
            cmd = "g++ " + test_file + " -o " + ext
            need_to_removed.append(ext)

            with tqdm(total=1.0, desc=test_file + ' compiling', initial=.25) as pbar:
                os.system(cmd)
                pbar.update(.75)
            print()
        digit = len(str(no))
        print()
        st = -1.0

        pt = '-' * 20 + test_file + '-' * 20
        cprint(pt, 'magenta')
        pt = (' ' * 13 + "...Bruteforcing...")
        print()
        cprint(f' # Test File  : ', 'yellow', end='')
        cprint(f'{test_file}', 'cyan')
        cprint(f' # Brute File : ', 'yellow', end='')
        cprint(f'{brute_file}', 'cyan')
        cprint(f' # Gen File   : ', 'yellow', end='')
        cprint(f'{gen_file}', 'cyan')
        cprint(f' # Stress     : ', 'yellow', end='')
        cprint(f'{no} ', 'cyan', end=' ')
        if no < 2:
            cprint('time', 'cyan')
        else:
            cprint('times', 'cyan')
        print()
        cprint(pt, 'blue')
        print()

        for i in range(no):
            pass
            iput = self.cmd_manager(gen_file, '', gen_ext, False)
            # print(iput)
            ans = self.cmd_manager(brute_file, iput, brute_ext, True)
            # print(ans)
            t = time.time()
            result = self.cmd_manager(test_file, iput, test_ext, True)
            # print(ans)
            t = time.time() - t
            cprint('  * ' + str(i + 1).zfill(digit) + ') ', 'yellow', end='')

            # if(iput == '4\n'):
            #     print(ans)
            #     print(result)
            #     break
            if t > st:
                st = t
            if result == ans:
                cprint('Passed...', 'green', end=' ')
            else:
                cprint('Failed...', 'red', end=' ')
                cprint(f'[ Time : {t:.4f} sec ]', 'cyan')
                self.different(iput, result, ans)
                print()
                cprint(' # Failed. :(', 'red')
                with open('hack.in', 'w') as f:
                    f.write(iput)
                with open('hack.out', 'w') as f:
                    f.write(ans)

                self.remove_unnecessary(need_to_removed)
                print()
                cprint('Do you want to add this case to your testcases list? (Y/N) : ', 'cyan', attrs=['bold'], end='')
                want = input()
                want = want.lower()
                if want == 'y' or want == 'yes':
                    # cprint('Test case added successfully.','green')
                    self.add_case(iput, ans)
                return

            cprint(f'[ Time : {t:.4f} sec ]', 'cyan')

        print()
        cprint(f' # Slowest : {st:.4f} sec.', 'blue')
        cprint(f' # Accepted.', 'green')

        self.remove_unnecessary(need_to_removed)

        print()
        pt = '-' * 20 + '-' * len(test_file) + '-' * 20
        cprint(pt, 'magenta')
