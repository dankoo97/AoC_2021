from advent import timer, read_file


def gauss(x):
    return (x*x + x) // 2


def potential(x1, y1, x2, y2):
    return x1 <= x2 and y1 >= y2


def in_range(x, y, x_range, y_range):
    return x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]


@timer
def p1(ins):

    return gauss(abs(int(ins.split('y=')[1].split('..')[0])) - 1)


@timer
def p2(ins):
    read = ins.split(', y=')
    target = {'x': tuple(int(i) for i in read[0][15:].split('..')), 'y': tuple(int(i) for i in read[1].split('..'))}

    # Count potential velocities
    v = 0

    # Find minimum x
    x = 1
    while not target['x'][0] <= gauss(x) <= target['x'][1]:
        x += 1

    # Part 1 solution
    y = abs(target['y'][0]) - 1

    # possible y range is lowest y target through abs(lowest) - 1
    for i in range(target['y'][0], y+1):

        # possible x range is the lowest gauss function greater than lowest target through highest target
        for j in range(x, target['x'][1] + 1):
            pos = 0, 0
            dx, dy = j, i

            # Brute force check
            # IF it still has potential
            while potential(*pos, target['x'][1], target['y'][0]):
                # If found
                if in_range(*pos, target['x'], target['y']):
                    v += 1
                    break
                pos = pos[0] + dx, pos[1] + dy
                dx = dx - 1 if dx > 0 else 0
                dy -= 1

    return v


f = read_file("./Input/Input17")
p1(f)
p2(f)
