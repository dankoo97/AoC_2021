from advent import read_file, timer


def adj(x, y):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if (dx or dy) and x+dx >= 0 and y+dy >= 0:
                yield x+dx, y+dy


def flash(x, y, octo, b):
    for dx, dy in adj(x, y):
        try:
            octo[dy][dx] += 1
            if octo[dy][dx] >= 10 and not b[dy][dx]:
                b[dy][dx] = True
                flash(dx, dy, octo, b)
        except:
            pass

@timer
def p1(ins):
    octo = [[int(i) for i in r] for r in f]
    t = 100
    s = 0

    for _ in range(t):
        b = [[False for i in range(10)] for j in range(10)]
        for y, row in enumerate(octo):
            for x in range(len(row)):
                octo[y][x] += 1
                if octo[y][x] >= 10 and not b[y][x]:
                    b[y][x] = True
                    flash(x, y, octo, b)

        for y in range(len(octo)):
            for x in range(len(octo[0])):
                if b[y][x]:
                    s += 1
                    octo[y][x] = 0

    # print(*[''.join(str(i) for i in row) for row in octo], sep='\n')

    return s


@timer
def p2(ins):
    octo = [[int(i) for i in r] for r in f]
    t = 0

    while True:
        t += 1
        b = [[False for i in range(10)] for j in range(10)]
        for y, row in enumerate(octo):
            for x in range(len(row)):
                octo[y][x] += 1
                if octo[y][x] >= 10 and not b[y][x]:
                    b[y][x] = True
                    flash(x, y, octo, b)

        for y in range(len(octo)):
            for x in range(len(octo[0])):
                if b[y][x]:
                    octo[y][x] = 0

        # print(t)
        # print(*octo, sep='\n')
        # print()

        if all(all(row) for row in b):
            return t

f = read_file("./Input/Input11").split('\n')
p1(f)
p2(f)
