from advent import read_file, timer
from heapq import heapify, heappop, heappush
from sys import maxsize
from collections import defaultdict


def reconstruct_path(current, came_from, g_score):
    total_path = [current]
    g = [g_score[current]]
    while current in came_from:
        current = came_from[current]
        total_path = [current] + total_path
        g = [g_score[current]] + g
    return total_path, g


class Room:
    def __init__(self, occupants, desired):
        self.occupants = occupants
        self.desired = desired

    def only_desired(self):
        return all(c == self.desired for c in self.occupants)

    def without_top(self):
        return Room(tuple(oc for oc in self.occupants[:-1]), self.desired)

    def add_top(self, top):
        return Room((*self.occupants, top), self.desired)

    def peek(self):
        return self[-1]

    def __len__(self):
        return len(self.occupants)

    def __getitem__(self, item):
        return self.occupants[item]

    def __eq__(self, other):
        return self.occupants == other.occupants and self.desired == other.desired

    def __hash__(self):
        return hash(self.occupants) + hash(self.desired)

    def copy(self):
        return Room(tuple(oc for oc in self.occupants), self.desired)

    def __bool__(self):
        return bool(self.occupants)

    def __repr__(self):
        return 'Room({}, {})'.format(self.occupants, self.desired)


class Hall:
    moves_cost = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
    }

    def __init__(self, hall=None):
        self.hall = hall if hall else tuple('.') * 11
        self.rooms = []
        self.room_size = 0

    def add_room(self, room):
        self.rooms.append(room)
        self.room_size = max((len(room), self.room_size))

    def ready_rooms(self):
        return [ready.only_desired() for ready in self.rooms]

    def is_sorted(self):
        return all((
            all(cell == '.' for cell in self.hall),
            all(room.only_desired() for room in self.rooms)
        ))

    def __str__(self):
        s = '#' * 13 + '\n' + '#' + ''.join(self.hall) + '#\n'
        for i in range(self.room_size - 1, -1, -1):
            s += '###'
            for j in range(4):
                try:
                    s += self.rooms[j][i] + '#'
                except IndexError:
                    s += '.' + '#'
            s += '##\n'

        s += '#' * 13 + ' Is sorted? ' + str(self.is_sorted()) + '\n'

        return s

    def __repr__(self):
        return str(self)

    def copy(self):
        h = Hall(tuple(cell for cell in self.hall))
        h.room_size = self.room_size
        for room in self.rooms:
            h.add_room(room.copy())

        return h

    def __eq__(self, other):
        if not isinstance(other, Hall):
            return False
        return all((
            all(a == b for a, b in zip(self.hall, other.hall)),
            all(a == b for a, b in zip(self.rooms, other.rooms))
        ))

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __hash__(self):
        return hash(self.hall) + sum(hash(room) for room in self.rooms)

    def solve(self):
        def h_func(h):
            s = 0
            for hall in (0, 1, 3, 5, 7, 9, 10):
                if h.hall[hall] != '.':
                    s += Hall.moves_cost[h.hall[hall]] * abs(hall - (2 + 2 * (ord(h.hall[hall]) - ord('A'))))
            for room in range(4):
                for i, occupant in enumerate(h.rooms[room]):
                    s += Hall.moves_cost[occupant] * (abs(2 * room + 2 - (2 + 2 * (ord(occupant) - ord('A')))) + h.room_size - i)
            return s

        open_set = [(h_func(self), self)]
        heapify(open_set)
        came_from = {}
        g_score = defaultdict(lambda: maxsize)
        f_score = defaultdict(lambda: maxsize)

        g_score[self] = 0
        f_score[self] = h_func(self)

        while open_set:
            curr = heappop(open_set)[1]
            # print(f_score[curr])
            if curr.is_sorted():
                return g_score[curr], reconstruct_path(curr, came_from, g_score)

            for hall in (0, 1, 3, 5, 7, 9, 10):
                for room in range(4):
                    if any((
                        curr.hall[hall] != curr.rooms[room].desired and curr.rooms[room].only_desired(),

                    )):
                        continue

                    if move := curr.move(hall, room):
                        h, i, p = move
                        temp = g_score[curr] + i * Hall.moves_cost[p]
                        if temp < g_score[h]:
                            came_from[h] = curr
                            g_score[h] = temp
                            f_score[h] = temp + h_func(h)
                            if h not in open_set:
                                heappush(open_set, (f_score[h], h))

        return -1, []

    def move_room_to_hall(self, hall, room):
        hall = Hall(tuple(cell if hall != i else self.rooms[room].peek() for i, cell in enumerate(self.hall)))
        hall.room_size = self.room_size
        for i, r in enumerate(self.rooms):
            if i == room:
                hall.add_room(r.without_top())
            else:
                hall.add_room(r.copy())
        return hall

    def move_hall_to_room(self, hall, room):
        c = self.hall[hall]
        hall = Hall(tuple(cell if hall != i else '.' for i, cell in enumerate(self.hall)))
        hall.room_size = self.room_size
        for i, r in enumerate(self.rooms):
            if i == room:
                hall.add_room(r.add_top(c))
            else:
                hall.add_room(r.copy())
        return hall

    def legal_move(self, hall, room, hall_to_room):
        if hall in (2, 4, 6, 8):
            return False

        if hall_to_room:
            b = self.hall[hall] == self.rooms[room].desired and self.rooms[room].only_desired()
        else:
            b = self.hall[hall] == '.'

        if hall < room * 2 + 2:
            return all(c == '.' for c in self.hall[hall+1:room * 2 + 2 + 1]) and b
        else:
            return all(c == '.' for c in self.hall[room * 2 + 2:hall]) and b

    def move(self, hall, room):
        if self.hall[hall] == '.':
            if self.legal_move(hall, room, False):
                return self.move_room_to_hall(hall, room), self.move_dist(hall, room), self.rooms[room].peek()
        else:
            if self.legal_move(hall, room, True):
                return self.move_hall_to_room(hall, room), self.move_dist(hall, room), self.hall[hall]
        return None

    def move_dist(self, hall, room):
        return abs(room * 2 + 2 - hall) + int(self.hall[hall] == '.') + self.room_size - len(self.rooms[room])


@timer
def p1(ins):
    # Initially solved by hand w/ some guess work (minimum with phasing through in the hallway is 11316)

    # Read input
    rooms = [line.strip('# ').split('#') for line in ins[2:-1]]
    r = [[r] for r in rooms[0]]
    for room in rooms[1:]:
        for i in range(4):
            r[i].append(room[i])
    rooms = [tuple(reversed(re)) for re in r]

    # Create initial hall and add rooms
    hall = Hall()
    for i in range(4):
        hall.add_room(Room(rooms[i], chr(ord('A') + i)))

    total, path = hall.solve()

    for p in range(len(path[0])):
        print(path[0][p])
        print(path[1][p])
        print('\n\n')

    return total


@timer
def p2(ins):
    # Read input
    ins = ins[:3] + "#D#C#B#A#\n#D#B#A#C#".split('\n') + ins[3:]

    rooms = [line.strip('# ').split('#') for line in ins[2:-1]]
    r = [[r] for r in rooms[0]]
    for room in rooms[1:]:
        for i in range(4):
            r[i].append(room[i])
    rooms = [tuple(reversed(re)) for re in r]

    # Create initial hall and add rooms
    hall = Hall()
    for i in range(4):
        hall.add_room(Room(rooms[i], chr(ord('A') + i)))

    total, path = hall.solve()

    for p in range(len(path[0])):
        print(path[0][p])
        print(path[1][p])
        print('\n\n')

    return total


if __name__ == '__main__':
    f = read_file("./Input/Input23").split('\n')
    # Approximate times on my machine
    # Approx 1:30
    p1(f)

    # Approx 2:10
    p2(f)
