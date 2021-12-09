from advent import timer, read_file


def adj(x, y):
    yield x+1, y
    yield x-1, y
    yield x, y+1
    yield x, y-1


def lowest(x, y, p):
    i = p[y][x]
    for dx, dy in adj(x, y):
        try:
            if i >= p[dy][dx]:
                return False
        except:
            pass

    return True


@timer
def p1(ins):
    points = []
    s = 0
    for row in ins:
        points.append([int(i) for i in row])

    for y in range(len(points)):
        for x in range(len(points[0])):
            if lowest(x, y, points):
                s += points[y][x] + 1

    return s


def basin_size(x, y, p):
    start = p[y][x]
    marked = set()
    current = set()
    current.add((x, y))

    while current:
        marked = set.union(marked, set(current))
        prev = current
        current = set()

        for xp, yp in prev:
            for dx, dy in adj(xp, yp):
                try:
                    if any(0 > i for i in (dx, dy)):
                        continue
                    i = p[dy][dx]
                    if i != 9 and (dx, dy) not in marked:
                        current.add((dx, dy))
                except:
                    pass

    return len(marked)


@timer
def p2(ins):
    points = []
    basins = []
    for row in ins:
        points.append([int(i) for i in row])

    for y in range(len(points)):
        for x in range(len(points[0])):
            if lowest(x, y, points):
                p = basin_size(x, y, points)
                basins.append(p)
                basins.sort(reverse=True)

                if len(basins) > 3:
                    basins = basins[:3]

    return basins[0] * basins[1] * basins[2]


f = read_file("./Input/Input09").split('\n')
p1(f)
p2(f)
