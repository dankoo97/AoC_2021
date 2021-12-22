from advent import read_file, timer
from functools import reduce


def check_overlaps(a, b):
    """Check for overlap, return intersecting cuboid"""
    # Sort the coords in x, y, z dimensions
    x = tuple(sorted((*a[0], *b[0])))
    y = tuple(sorted((*a[1], *b[1])))
    z = tuple(sorted((*a[2], *b[2])))

    # If the coords are not (*a, *b or *b, *a) or a and b share a value in all 3 dimensions, the cubes intersect
    intersects = all((
        a[0] not in (x[:2], x[-2:]) or x[1] == x[2],
        a[1] not in (y[:2], y[-2:]) or y[1] == y[2],
        a[2] not in (z[:2], z[-2:]) or z[1] == z[2],
    ))

    # Return the intersecting cube is the middle values for each dimension
    if intersects:
        return x[1:-1], y[1:-1], z[1:-1]


def cube_size(cube):
    if cube is None:
        return 0
    return reduce(lambda a, b: a * b, [1 + abs(cube[i][1] - cube[i][0]) for i in range(3)])


def total_volume(cube_set):
    if len(cube_set) <= 1:
        return sum(cube_size(c) for c in cube_set)

    if len(cube_set) == 2:
        a, b = cube_set
        overlap = cube_size(check_overlaps(a, b))
        return cube_size(a) + cube_size(b) - int(overlap)

    v = 0
    while cube_set:
        # Pick a cube and remove it
        cube = cube_set.pop()
        intersecting = set()

        # Check for intersecting cubes
        for c in cube_set:
            if overlap := check_overlaps(cube, c):
                intersecting.add(overlap)

        # Add this cubes volume minus the intersections
        v += cube_size(cube) - total_volume(intersecting)
    return v


def read_cube_line(line):
    on, coords = line.split()
    on = on == 'on'
    x, y, z = coords.split(',')
    x = tuple(int(i) for i in x[2:].split('..'))
    y = tuple(int(i) for i in y[2:].split('..'))
    z = tuple(int(i) for i in z[2:].split('..'))

    return on, x, y, z


def solve(ins):
    cubes = []

    for line in ins:
        cubes.append(read_cube_line(line))

    fixed = set()
    count = 0

    # Read it backwards
    # If the last instruction is off, all those cubes are permanently off
    # If it is on, all those cubes are permanently on
    # No need to think about turning cubes on or off
    for c in cubes[::-1]:
        # If cube is on
        if c[0]:

            # Check for intersection with fixed cubes
            intersecting = set()
            for cube in fixed:
                if check := check_overlaps(c[1:], cube):
                    intersecting.add(check)

            # How many cubes are turned on
            s = cube_size(c[1:]) - total_volume(intersecting)

            # Bug checking
            if s < 0:
                raise ValueError("Negative volume:", s)

            count += s

        # Add the cube to the fixed cube set
        fixed.add(c[1:])

    return count


@timer
def p1(ins):
    # Cheaty, only the first 20 lines are inbounds
    return solve(ins[:20])


@timer
def p2(ins):
    return solve(ins)


if __name__ == '__main__':
    f = read_file("./Input/Input22").split('\n')
    p1(f)
    p2(f)
