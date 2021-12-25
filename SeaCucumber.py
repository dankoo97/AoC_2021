from advent import read_file, timer


@timer
def p1(ins):
    DEBUG = 0
    east, south = set(), set()
    sea_floor_size = len(ins[0]), len(ins)
    for y, row in enumerate(ins):
        for x, cell in enumerate(row):
            if cell == '>':
                east.add((x, y))
            elif cell == 'v':
                south.add((x, y))

    flag = True
    count = 0

    while flag:
        if DEBUG:
            print(count)
            for i in range(sea_floor_size[1]):
                print()
                for j in range(sea_floor_size[0]):
                    if (j, i) in east:
                        print('>', end='')
                    elif (j, i) in south:
                        print('v', end='')
                    else:
                        print('.', end='')
            print('\n\n')

        flag = False
        new = set()

        for x, y in east:
            next = ((x + 1) % sea_floor_size[0], y)
            if next in east or next in south:
                new.add((x, y))
            else:
                new.add(next)
                flag = True

        east = new
        new = set()

        for x, y in south:
            next = (x, (y + 1) % sea_floor_size[1])
            if next in east or next in south:
                new.add((x, y))
            else:
                new.add(next)
                flag = True

        south = new

        count += 1

    return count


f = read_file("./Input/Input25").split()
p1(f)
