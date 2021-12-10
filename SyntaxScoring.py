from advent import read_file, timer

def insort(lst, val):
    for i in range(len(lst)):
        if val < lst[i]:
            lst.insert(i, val)
            return
    lst.append(val)


@timer
def p1(ins):
    cl = {'(': ')', '[': ']', '{': '}', '<': '>'}
    corrupt = {')': 3, ']': 57, '}': 1197, '>': 25137}
    s = 0
    for ln in ins:

        stack = []

        for c in ln:
            if c in cl:
                stack.append(c)
            elif cl[stack[-1]] == c:
                stack.pop()
                continue
            else:
                s += corrupt[c]
                break

    return s


@timer
def p2(ins):
    cl = {'(': ')', '[': ']', '{': '}', '<': '>'}
    complete = {'(': 1, '[': 2, '{': 3, '<': 4}
    total = []
    for ln in ins:
        stack = []
        corrupt = False

        for c in ln:
            if c in cl:
                stack.append(c)
            elif cl[stack[-1]] == c:
                stack.pop()
                continue
            else:
                corrupt = True
                break

        if not corrupt:
            s = 0
            for c in stack[::-1]:
                s *= 5
                s += complete[c]

            insort(total, s)


    return total[len(total) // 2]


f = read_file("./Input/Input10").split()
p1(f)
p2(f)
