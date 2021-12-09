from advent import read_file, timer


@timer
def p1(ins):
    crabs = [int(i) for i in ins]
    crabs.sort()

    s = 0
    m = crabs[len(crabs) // 2] # Median

    for c in crabs:
        s += abs(m - c)

    return s


@timer
def p2(ins):
    def crab_fuel(a):
        s = 0
        for c in crabs:
            s += abs(a-c) * (abs(a-c) + 1) // 2

        return s

    crabs = [int(i) for i in ins]
    crabs.sort()

    a0 = sum(crabs) // len(crabs) # Average, should be pretty close
    a1 = a0 + 1

    b0, b1 = crab_fuel(a0), crab_fuel(a1)

    if b0 < b1:
        da = -1
        prev = b1
        curr = b0
        a = a0
    else:
        da = 1
        prev = b0
        curr = b1
        a = a1

    while curr < prev:
        a += da
        prev = curr
        curr = crab_fuel(a)

    return prev


f = read_file("./Input/Input07").split(',')
p1(f)
p2(f)
