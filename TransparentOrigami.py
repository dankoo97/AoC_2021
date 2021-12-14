from advent import read_file, timer


def fold(paper, dim, f):
    new_paper = set()
    if dim == 'y':
        for x, y in paper:
            if y > f:
                new_paper.add((x, (f << 1) - y))
            else:
                new_paper.add((x, y))

    else:
        for x, y in paper:
            if x > f:
                new_paper.add(((f << 1) - x, y))
            else:
                new_paper.add((x, y))

    return new_paper


@timer
def p1(ins):
    coords, folds = ins.split('\n\n')
    paper = set()
    for coord in coords.split('\n'):
        x, y = [int(i) for i in coord.split(',')]
        paper.add((x, y))

    f = folds.split('\n')[0]
    dim, f = f.split('=')
    dim = dim[-1]
    f = int(f)

    paper = fold(paper, dim, f)

    return len(paper)


@timer
def p2(ins):
    coords, folds = ins.split('\n\n')
    paper = set()
    for coord in coords.split('\n'):
        x, y = [int(i) for i in coord.split(',')]
        paper.add((x, y))

    prev, curr = 0, len(paper)
    s = c = 0

    folds = folds.split('\n')
    for f in folds:
        dim, fold_line = f.split('=')
        dim = dim[-1]
        fold_line = int(fold_line)
        paper = fold(paper, dim, fold_line)

        # For finding the ratio of overlaps, 15% of dots on a fold overlap.
        # prev = curr
        # curr = len(paper)
        # s += curr / prev
        # c += 1

    # print(s / c)
    max_x = max(paper, key=lambda k: k[0])
    max_y = max(paper, key=lambda k: k[1])

    s = ''

    # Edited characters from example for readability
    for y in range(max_y[1]+1):
        s += '\n'
        for x in range(max_x[0]+1):
            s += ('#' if (x, y) in paper else ' ') + ' '

    return s


f = read_file("./Input/Input13")
p1(f)
p2(f)
