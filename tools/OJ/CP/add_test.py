import os

from termcolor import colored as clr, cprint


class Cp_add_test:

    @property
    def take_input(self):
        content = ''
        while True:
            try:
                line = input()
            except EOFError:
                break
            content += line + '\n'

        return content

    def test_print(self, name, value):
        pt = '-' * 22 + name + '-' * 22
        cprint(pt, 'magenta')
        value = value.split(sep='\n')
        for x in value:
            x = '  ' + x
            print(x)

    def add_case(self, no=1, name='Custom-'):
        """  function for adding testcases """
        try:
            pt = '-' * 20 + '-' * 10 + '-' * 20
            cprint(pt, 'magenta')
            pt = (' ' * 17 + "...Adding Testcase..." + '\n')
            print(clr(pt, 'blue'))

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

            cprint('Enter the input(Press Ctrl+d or Ctrl+z after done):', 'yellow')
            x = self.take_input

            cprint('Enter the output(Press Ctrl+d or Ctrl+z after done):', 'yellow')
            y = self.take_input

            fileName_in = name + str(no).zfill(2) + '.in'
            fileName_out = name + str(no).zfill(2) + '.out'
            print()

            self.test_print(fileName_in, x)
            self.test_print(fileName_out, y)

            cprint('-' * 55, 'magenta')

            cprint("Do you want to add this testcase(y/n) :", 'cyan', end='')
            confirm = input().lower()

            positive = ['y', 'yes']
            if confirm in positive:
                pass

            else:
                cprint("Cancelled.", 'red')
                return

            no += 1
            with open(os.path.join(path_name, fileName_in), 'w') as fin:
                fin.write(x)
            with open(os.path.join(path_name, fileName_out), 'w') as fout:
                fout.write(y)

            cprint('Testcase added Successfully. :D', 'green', attrs=['bold'])

            pt = '-' * 20 + '-' * 10 + '-' * 20
            cprint(pt, 'magenta')
        except:
            cprint("Can't add testcase. :( ", 'red', attrs=['bold'])
