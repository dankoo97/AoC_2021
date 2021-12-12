from advent import read_file, timer


def adj(x, y):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if (dx or dy) and x+dx >= 0 and y+dy >= 0:
                yield x+dx, y+dy


def flash(x, y, octo, b):
    b.add((x, y))
    for dx, dy in adj(x, y):
        if dx < 0 or dy < 0:
            continue
        try:
            octo[dy][dx] += 1
            if octo[dy][dx] >= 10 and (dx, dy) not in b:
                flash(dx, dy, octo, b)
        except IndexError:
            pass


def tick(octo):
    """Returns the number of flashing octopus"""
    b = set()
    for y in range(len(octo)):
        for x in range(len(octo[0])):
            octo[y][x] += 1
            if octo[y][x] >= 10 and (x, y) not in b:
                flash(x, y, octo, b)

    for x, y in b:
        octo[y][x] = 0

    return len(b)


@timer
def p1(ins, t=None):
    octo = [[int(i) for i in r] for r in ins]
    t = 100 if t is None else t
    s = 0

    for _ in range(t):
        s += tick(octo)

    return s


@timer
def p2(ins):
    octo = [[int(i) for i in r] for r in ins]
    t = 0

    while True:
        t += 1
        if tick(octo) == 100:
            return t


f = read_file("./Input/Input11").split('\n')
p1(f)
p2(f)
