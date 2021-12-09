from advent import read_file, timer


@timer
def p1(ins):
    horz = 0
    depth = 0
    c = ""
    i = 0

    for com in ins.split('\n'):
        c, i = com.split()
        i = int(i)
        if c == 'forward':
            horz += i
        elif c == 'up':
            depth -= i
        elif c == 'down':
            depth += i

    return depth * horz


@timer
def p2(ins):
    horz = 0
    depth = 0
    c = ""
    i = 0
    aim = 0

    for com in ins.split('\n'):
        c, i = com.split()
        i = int(i)
        if c == 'forward':
            horz += i
            depth += i * aim
        elif c == 'up':
            aim -= i
        elif c == 'down':
            aim += i

    return depth * horz


f = read_file("./Input/Input02")
p1(f)
p2(f)