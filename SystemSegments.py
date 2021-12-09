from advent import read_file, timer


@timer
def p1(ins):
    code = ins.split('\n')
    s = 0

    check = (2, 4, 3, 7)

    for line in code:
        fix = line.split('|')[1].strip()
        out = [len(c) for c in fix.split()]
        for c in check:
            s += out.count(c)

    return s


@timer
def p2(ins):
    code = ins.split('\n')
    s = 0

    easy = {2: 1, 4: 4, 3: 7, 7: 8}

    for line in code:
        sp, out = (l.split() for l in line.split('|'))
        d = dict()

        for p in sp:
            length = len(p)
            if length in easy:
                d[easy[length]] = p

        for p in sp:
            if len(p) == 5 and len(set.intersection(set(d[1]), set(p))) == 2:
                d[3] = p
            if len(p) == 6 and len(set.intersection(set(d[1]), set(p))) == 1:
                d[6] = p
            elif len(p) == 6 and len(set(d[4]) - set(p)) == 0:
                d[9] = p
            elif len(p) == 6:
                d[0] = p

        for p in sp:
            if len(p) == 5 and p not in d.values():
                if len(set(d[6]) - set(p)) == 1:
                    d[5] = p
                else:
                    d[2] = p

        out_d = {frozenset(k): v for v, k in d.items()}
        st = ''

        for c in out:
            st += str(out_d[frozenset(c)])

        s += int(st)

    return s


f = read_file("./Input/Input08")
p1(f)
p2(f)
