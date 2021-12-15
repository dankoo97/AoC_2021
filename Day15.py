from advent import read_file, timer
from sys import setrecursionlimit

setrecursionlimit(3000)


def adjacent(curr):
    yield curr[0] + 1, curr[1]
    yield curr[0] - 1, curr[1]
    yield curr[0], curr[1] + 1
    yield curr[0], curr[1] - 1


def get_val(curr, cave):
    mod_x = curr[0] % len(cave[0])
    mod_y = curr[1] % len(cave)
    val = (cave[mod_y][mod_x] + curr[0] // len(cave[0]) + curr[1] // len(cave))
    if 9 < val:
        val %= 9

    return val


def best_path(cave, dest):
    """Dijkstrra's algo"""
    visited = {}
    tentative = {(0, 0): 0}

    while True:
        curr = min(tentative, key=tentative.get)
        val = tentative[curr]
        # print("Checking:", curr, ":", val)
        if curr == dest:
            return val
        for adj in adjacent(curr):
            if adj in visited or adj[0] < 0 or dest[0] < adj[0] or adj[1] < 0 or dest[1] < adj[1]:
                continue
            if adj in tentative:
                tentative[adj] = min((val + get_val(adj, cave), tentative[adj]))
            else:
                tentative[adj] = val + get_val(adj, cave)

        visited[curr] = val
        del tentative[curr]


@timer
def p1(ins):
    cave = [[int(i) for i in row] for row in ins]

    dest = (len(cave) - 1, len(cave[0]) - 1)

    return best_path(cave, dest)


@timer
def p2(ins):
    cave = [[int(i) for i in row] for row in ins]

    dest = (5 * len(cave) - 1, 5 * len(cave[0]) - 1)

    return best_path(cave, dest)


f = read_file("./Input/Input15").split('\n')
p1(f)
p2(f)
