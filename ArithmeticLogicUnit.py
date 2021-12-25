from advent import read_file, timer


class ALU:

    def __init__(self, func=None):
        self.vars = {k: 0 for k in 'wxyz'}
        self.func = func if func is not None else input

    def inp(self, var):
        self.vars[var] = int(self.func())

    def add(self, var, val):
        try:
            v = int(val)
        except ValueError:
            v = self.vars[val]
        self.vars[var] += v

    def mul(self, var, val):
        try:
            v = int(val)
        except ValueError:
            v = self.vars[val]
        self.vars[var] *= v

    def div(self, var, val):
        try:
            v = int(val)
        except ValueError:
            v = self.vars[val]
        self.vars[var] //= v

    def mod(self, var, val):
        try:
            v = int(val)
        except ValueError:
            v = self.vars[val]
        self.vars[var] %= v

    def eql(self, var, val):
        try:
            v = int(val)
        except ValueError:
            v = self.vars[val]
        self.vars[var] = int(self.vars[var] == v)

    def clear(self):
        self.vars = {k: 0 for k in 'wxyz'}

    def __str__(self):
        return str(self.vars)


class Number:
    def __init__(self, n):
        self.number = str(n)
        self.i = -1

    def next(self):
        self.i += 1
        return self.number[self.i]

    def __str__(self):
        return str(self.number)

    def __repr__(self):
        return str(self)


def solve(n, prog, debug=None):
    instructions = {
        'inp': ALU.inp,
        'add': ALU.add,
        'mul': ALU.mul,
        'div': ALU.div,
        'mod': ALU.mod,
        'eql': ALU.eql,
    }
    n = Number(n)
    a = ALU(n.next)

    for instruct in prog.split('\n'):
        f, *args = instruct.split()
        instructions[f](a, *args)
        if debug:
            print(instruct)
            print(a)
            print()

    return a.vars['z']



@timer
def p1(ins):
    # Solution is based on solving the individual input to find patterns and constraints
    # n[0] = n[13] + 8
    # n[1] = n[12] + 2
    # n[2] = n[3] - 4
    # n[3] = n[2] + 4
    # n[4] = n[11] - 1
    # n[5] = n[6] + 3
    # n[6] = n[5] - 3
    # n[7] = n[8] - 6
    # n[8] = n[7] + 6
    # n[9] = n[10]
    # n[10] = n[9]
    # n[11] = n[4] + 1
    # n[12] = n[1] - 2
    # n[13] = n[0] - 8
    n = Number(99598963999971)
    return {'z': solve(n, ins), 'solution': n}


@timer
def p2(ins):

    n = Number(93151411711211)
    return {'z': solve(n, ins), 'solution': n}


f = read_file("./Input/Input24")
p1(f)
p2(f)
