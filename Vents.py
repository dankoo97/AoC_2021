from advent import read_file, timer
from collections import defaultdict


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def read(self, s):
        self.x, self.y = (int(i) for i in s.split(','))

    def __str__(self):
        return 'x: ' + str(self.x) + '    y: ' + str(self.y)


class Line:
    def __init__(self, p1=None, p2=None):
        try:
            self.straight = self.p1.x == self.p2.x or self.p1.y == self.p2.y
        except:
            self.straight = False

        try:
            self.diag = abs(self.p1.x - self.p2.x) == abs(self.p1.y - self.p2.y)
        except:
            self.diag = False

        self.p1 = p1
        self.p2 = p2

    def read(self, s):
        s = s.split(' -> ')
        self.p1 = Point()
        self.p2 = Point()

        self.p1.read(s[0])
        self.p2.read(s[1])
        self.straight = self.p1.x == self.p2.x or self.p1.y == self.p2.y
        self.diag = abs(self.p1.x - self.p2.x) == abs(self.p1.y - self.p2.y)

    def iterate(self, d=False):
        startx = self.p1.x
        endx = self.p2.x
        starty = self.p1.y
        endy = self.p2.y
        slope = dict()

        if self.straight:
            slope['x'] = 0 if startx == endx else (-1) ** (startx > endx)
            slope['y'] = 0 if starty == endy else (-1) ** (starty > endy)
        elif self.diag and d:
            slope['x'] = 1 if startx < endx else -1
            slope['y'] = 1 if starty < endy else -1

        x = startx
        y = starty

        while x != endx or y != endy:
            yield x, y
            x += slope['x']
            y += slope['y']

        yield x, y

    def __str__(self):
        return str(self.p1) + '\n' + str(self.p2) + '\n'


@timer
def p1(ins):
    lines = defaultdict(int)
    for line in ins:
        ln = Line()
        ln.read(line)
        if ln.straight:
            for p in ln.iterate():
                lines[p] += 1

    return len(tuple(i for i in lines.values() if i >= 2))


@timer
def p2(ins):
    lines = defaultdict(int)
    for line in ins:
        ln = Line()
        ln.read(line)
        if ln.straight or ln.diag:
            for p in ln.iterate(True):
                lines[p] += 1

    return len(tuple(i for i in lines.values() if i >= 2))


f = read_file("./Input/Input05").strip().split('\n')
p1(f)
p2(f)
