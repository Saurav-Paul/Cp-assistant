import os

from termcolor import colored as clr, cprint


class CpAddTest:
    """
     This class handles adding testcases
    """

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

    @staticmethod
    def test_print(name, value):
        pt = '-' * 22 + name + '-' * 22
        cprint(pt, 'magenta')
        value = value.split(sep='\n')
        for x in value:
            x = '  ' + x
            print(x)

    def add_case(self, name='Custom-'):
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

            filename_in = name + str(no).zfill(2) + '.in'
            filename_out = name + str(no).zfill(2) + '.out'
            print()

            self.test_print(filename_in, x)
            self.test_print(filename_out, y)

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
            with open(os.path.join(path_name, filename_in), 'w') as fin:
                fin.write(x)
            with open(os.path.join(path_name, filename_out), 'w') as f_out:
                f_out.write(y)

            cprint('Testcase added Successfully. :D', 'green', attrs=['bold'])

            pt = '-' * 20 + '-' * 10 + '-' * 20
            cprint(pt, 'magenta')
        except:
            cprint("Can't add testcase. :( ", 'red', attrs=['bold'])
