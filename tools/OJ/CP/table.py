from termcolor import colored as clr, cprint
from itertools import zip_longest
import os


class Table:
    try:
        columns, rows = os.get_terminal_size(0)
        columns -= 15
    except:
        columns = 100
    box_weight = columns // 2

    table_color = 'white'
    keyword = 'yellow'
    accepted = 'green'
    wrong = 'red'
    information = 'white'

    dif_sign = clr('|', table_color, attrs=['bold'])

    def multiple(self, n, value=' '):
        s = value * n
        return s

    def separator(self, value='-'):
        cprint(self.multiple(self.box_weight * 2 + 5 + 8, clr(value, self.table_color, attrs=['bold'])),
               self.table_color)

    def header(self, col1, col2):

        self.separator()

        print(self.dif_sign + clr(' LN ', self.keyword) + self.dif_sign, end='')

        before = (self.box_weight - len(col1)) / 2
        before = int(before)
        after = self.box_weight - before - len(col1)

        print(self.multiple(before, ' ') + clr(col1, self.keyword) + self.multiple(after, ' '), end='')
        print(self.dif_sign, end='')

        print(clr(' LN ', self.keyword) + self.dif_sign, end='')

        before = (self.box_weight - len(col2)) / 2
        before = int(before)
        after = self.box_weight - before - len(col2)

        print(self.multiple(before) + clr(col2, self.keyword) + self.multiple(after), end='')
        print(self.dif_sign, end='')

        print()

        self.separator()

    def line_print(self, no, x, y):

        pt = []

        for o, e in zip_longest(x, y, fillvalue=''):
            if (o == e):
                pt.append(clr(o, self.accepted))
            else:
                pt.append(clr(o, self.wrong))

        sx = len(x)
        sy = len(y)
        curr = 0

        xNull = False
        yNull = False

        if x == '(#$null$#)':
            xNull = True

        if y == '(#$null$#)':
            yNull = True

        smax = max(sx, sy)
        line_col = 'cyan'

        if x != y:
            line_col = 'red'

        while curr <= smax:

            print(self.dif_sign + ' ' + clr(no, line_col) + ' ' * (3 - len(no)) + self.dif_sign, end='')
            tx = ''
            if xNull == True:
                tx = clr('(null)', self.information) + ' ' * (self.box_weight - 6)
            else:
                for i in range(curr, curr + self.box_weight):
                    if i < sx:
                        tx += pt[i]
                    else:
                        tx += ' ' * (self.box_weight - (i - curr))
                        break

            print(tx + self.dif_sign, end='')

            print(' ' + clr(no, 'cyan') + ' ' * (3 - len(no)) + self.dif_sign, end='')
            tx = ''
            if yNull == True:
                tx = clr('(null)', self.information) + ' ' * (self.box_weight - 6)
            else:
                for i in range(curr, curr + self.box_weight):
                    if i < sy:
                        tx += clr(y[i], self.accepted)
                    else:
                        tx += ' ' * (self.box_weight - (i - curr))
                        break

            print(tx + self.dif_sign)

            curr += self.box_weight
            no = ''

    def print(self, output, expected, col1='Output', col2='Expected'):

        self.header(col1, col2)

        xempty = False
        yempty = False

        if output == '':
            xempty = True

        if expected == '':
            yempty = True
        x = output.split(sep='\n')
        y = expected.split(sep='\n')

        sx = len(x)
        sy = len(y)

        total_line = max(sx, sy)

        for no in range(total_line):
            try:
                vx = x[no]
            except:
                xempty = True
            try:
                vy = y[no]
            except:
                yempty = True

            if xempty:
                vx = '(#$null$#)'
            if yempty:
                vy = '(#$null$#)'
            self.line_print(str(no + 1), vx, vy)

        self.separator()
