from advent import read_file, timer
from collections import Counter


class Cave:
    def __init__(self, cave):
        self.cave = cave
        self.big = cave.isupper()
        self.adjacent = set()
        self.paths = {}

    def __eq__(self, other):
        return self.cave == other.cave

    def __hash__(self):
        return hash(self.cave)

    def connect(self, other):
        self.adjacent.add(other)
        other.adjacent.add(self)

    def __str__(self):
        return str(self.cave) + "\n" + str(self.adjacent)

    def __repr__(self):
        return "Cave(" + self.cave + ")"


def search(start, end, visited, real_start=None):
    paths = set()

    for cave in start.adjacent:
        if cave is end:
            paths.add((start, end))
            continue

        if real_start:
            nv = visited | {}
            if start not in nv:
                nv[start] = int(not start.big)
            elif nv[start] == 1:
                nv[start] = 2
        else:
            nv = visited | {start: not start.big}

        if cave in nv and nv[cave]:
            if not real_start or 2 in nv.values() or cave is real_start:
                continue

        # Possible Optimization: Memoization
        # if cave.paths:
        #     for path in cave.paths:
        #         if all(c.big for c in set(nv).intersection(set(path))):
        #             paths.add((start, *path))
        #         elif not real_start or 2 in nv.values():
        #             continue
        #         else:
        #             check = Counter((start, *path))
        #             b = False
        #             for c, i in check:
        #                 if not c.big and i == 2:
        #                     if b:
        #                         break
        #                     b = True
        #             else:
        #                 paths.add((start, *path))
        #     continue

        for p in search(cave, end, nv, real_start):
            paths.add((start, *p))

    start.paths[end] = paths
    return paths


def parse(ins):
    caves = dict()
    for conn in ins.split('\n'):
        a, b = conn.split('-')
        if a not in caves:
            caves[a] = Cave(a)
        if b not in caves:
            caves[b] = Cave(b)

        Cave.connect(caves[a], caves[b])

    return caves


@timer
def p1(ins):
    caves = parse(ins)

    paths = search(caves["start"], caves["end"], {})

    return len(paths)


@timer
def p2(ins):
    caves = parse(ins)

    paths = search(caves["start"], caves["end"], {}, caves["start"])

    return len(paths)


f = read_file("./Input/Input12")
p1(f)
p2(f)
