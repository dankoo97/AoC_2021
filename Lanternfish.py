from advent import read_file, timer
from collections import Counter


@timer
def p1(ins):
    fish = [int(i) for i in ins]
    t = 80

    for i in range(t):
        nf = 0
        for j in range(len(fish)):
            fish[j] -= 1
            if fish[j] == -1:
                nf += 1
                fish[j] = 6

        fish += [8] * nf

    return len(fish)


@timer
def p2(ins):
    # After one iteration for any starting value
    fish_d = [(6, 8), (0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,)]
    t = 256

    # IF we know the result of any arbitrary fish timer f after n iterations
    # THEN we can use this result to calculate the result after another n iterations for a given list of fish
    # THEREFORE if we know all results after n iterations, n*2 iterations is relatively trivial
    n = 1
    while n < (t // 2):  # BUT 256 is still too large, so we cheat a bit

        # create a new list to store results
        nf = []

        # Find the next iteration based on the current
        for f in fish_d:
            tup = []

            # Count how many fish on each timer and add that many from the current result
            for i in range(9):
                tup += fish_d[i] * f.count(i)

            # Add to new result list
            nf.append(tuple(tup))

        # Replace old results with new
        fish_d = nf

        # Keep track of iteration count
        n *= 2

    # Create a cheaty new list to calculate the length rather than the result for final iteration
    nf = []
    for f in fish_d:
        nf.append(0)
        for i in range(9):
            nf[-1] += f.count(i) * len(fish_d[i])

    # store result
    fish_d = nf

    # Get input and start counter
    fish = [int(i) for i in ins]
    s = 0

    # Get count * result length
    for i in range(9):
        s += fish_d[i] * fish.count(i)

    return s


@timer
def alt(ins, t):
    c = Counter(int(i) for i in ins)

    for i in range(t):
        v0 = c[0]
        del c[0]

        nf = Counter()
        for k, v in c.items():
            nf[k-1] = v

        nf[6] += v0
        nf[8] = v0

        c = nf

    return sum(c.values())


f = read_file("./Input/Input06").strip().split(',')
p1(f)
p2(f)
print()
alt(f, 80)
alt(f, 256)
