from advent import read_file, timer


@timer
def p1(ins):
    # count the instances of 1 at a position, store in a list
    binary = [0] * len(ins[0])
    for line in ins:
        for i, c in enumerate(line):
            binary[i] += (c == '1')

    # gamma and epsilon are 1s-complement of each other ie. add up to 0b111111111111
    g = int(''.join('1' if c*2 > len(ins) else '0' for c in binary), 2)
    e = (2**len(ins[0])) - 1 - g

    # Check for complement
    print(bin(g+e))
    print("0b111111111111")

    return g*e


@timer
def p2(ins):
    def comp(s, func, pos=0):
        # base case
        if len(s) == 1 or len(ins[0]) == pos:
            return s

        # Create parallel sets for values at position pos
        s0, s1 = set(), set()

        # Iterate through set adding binary line to appropriate set
        for line in s:
            if line[pos] == '1':
                s1.add(line)
            else:
                s0.add(line)

        # Recurse
        return comp(s1 if func(len(s1), len(s0)) else s0, func, pos+1)

    #  Create sets for oxygen and co2
    oxg = set(ins)
    co2 = set(ins)

    # Iterate recursively
    oxg = comp(oxg, int.__ge__)
    co2 = comp(co2, int.__lt__)

    print(oxg)
    print(co2)

    return int(''.join(oxg), 2) * int(''.join(co2), 2)


f = read_file("./Input/Input03").split()
p1(f)
p2(f)
