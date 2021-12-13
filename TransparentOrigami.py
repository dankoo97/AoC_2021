from advent import read_file, timer


def fold(paper, dim, f):
    if dim == 'y':
        new_paper = set()
        for x, y in paper:
            if y > f:
                new_paper.add((x, (f << 1) - y))
            else:
                new_paper.add((x, y))

    else:
        new_paper = set()
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

    folds = folds.split('\n')
    for f in folds:
        dim, fold_line = f.split('=')
        dim = dim[-1]
        fold_line = int(fold_line)

        paper = fold(paper, dim, fold_line)

    max_x = max(paper, key=lambda k: k[0])
    max_y = max(paper, key=lambda k: k[1])

    s = ''

    # Edited for readability
    for y in range(max_y[1]+1):
        s += '\n'
        for x in range(max_x[0]+1):
            s += ('#' if (x, y) in paper else ' ') + ' '

    return s


f = read_file("./Input/Input13")
p1(f)
p2(f)
