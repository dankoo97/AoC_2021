from advent import read_file, timer
from collections import defaultdict
from heapq import heapify, heappop, heappush
import sys


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


def reconstruct_path(current, came_from):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path = [current] + total_path
    return total_path


def dijkstra(cave, dest):
    """Dijkstra's algo"""
    visited = {}
    came_from = {}
    tentative = defaultdict(lambda: sys.maxsize)
    tentative[(0, 0)] = 0

    while True:
        curr = min(tentative, key=tentative.get)
        val = tentative[curr]
        # print("Checking:", curr, ":", val)
        if curr == dest:
            return val, reconstruct_path(curr, came_from)
        for adj in adjacent(curr):
            if adj in visited or not 0 <= adj[0] <= dest[0] or not 0 <= adj[1] <= dest[1]:
                continue
            temp = val + get_val(adj, cave)
            if temp < tentative[adj]:
                came_from[adj] = curr
                tentative[adj] = temp

        visited[curr] = val
        del tentative[curr]


def a_star(cave, dest):
    def h_func(a):
        # Manhattan distance
        return (dest[0] - a[0]) + (dest[1] - a[1])

    open_set = [(h_func((0, 0)), (0, 0))]
    heapify(open_set)
    came_from = {}
    g_score = defaultdict(lambda: sys.maxsize)
    f_score = defaultdict(lambda: sys.maxsize)

    g_score[(0, 0)] = 0
    f_score[(0, 0)] = h_func((0, 0))

    while open_set:
        curr = heappop(open_set)[1]
        if curr == dest:
            return g_score[curr], reconstruct_path(curr, came_from)

        for adj in adjacent(curr):
            if not 0 <= adj[0] <= dest[0] or not 0 <= adj[1] <= dest[1]:
                continue
            temp = g_score[curr] + get_val(adj, cave)
            if temp < g_score[adj]:
                came_from[adj] = curr
                g_score[adj] = temp
                f_score[adj] = temp + h_func(adj)
                if adj not in open_set:
                    heappush(open_set, (f_score[adj], adj))

    return -1, []


@timer
def p1(ins):
    cave = [[int(i) for i in row] for row in ins]

    dest = (len(cave) - 1, len(cave[0]) - 1)

    func = a_star
    # func = dijkstra

    val, path = func(cave, dest)

    return val


@timer
def p2(ins):
    cave = [[int(i) for i in row] for row in ins]

    dest = (5 * len(cave) - 1, 5 * len(cave[0]) - 1)

    func = a_star
    # func = dijkstra

    val, path = func(cave, dest)

    return val


f = read_file("./Input/Input15").split('\n')
p1(f)
p2(f)
