from advent import read_file, timer


@timer
def p1(file):
    c = 0
    prev = 200
    for i in file:
        i = int(i)
        if i > prev:
            c += 1
        prev = i

    return c


@timer
def p2(file):
    nums = tuple(int(i) for i in file)
    cnt = 0
    for i, n in enumerate(nums[3:], 0):
        # Compare nums[i+3] and nums[i]
        if n > nums[i]:
            cnt += 1

    return cnt


f = read_file("./Input/Input01").split('\n')
p1(f)
p2(f)
