from advent import timer, read_file
from collections import Counter, defaultdict


def get_rules(ins):
    """Gets rules from input"""
    rules = {}
    for line in ins[1].split('\n'):
        a, b = line.split(' -> ')
        rules[a] = a[0] + b

    return rules


@timer
def p1(ins):
    template = ins[0]
    rules = get_rules(ins)
    t = 10

    # Naive solution
    for _ in range(t):
        new_template = ''
        for i in range(len(template) - 1):
            new_template += rules[template[i: i+2]]

        template = new_template + template[-1]

    count = Counter(template)

    return max(count.values()) - min(count.values())


@timer
def p2(ins):
    template = ins[0]
    rules = get_rules(ins)
    rules_expansion = {}
    counts = {}
    t = 40

    # Find what a polymer starting with any arbitrary rule will end up being after half the days
    for r in rules:
        # Keep track of how fast it calculates 20 iterations
        print(r)
        temp = r
        for _ in range(t >> 1):
            nt = ''
            for i in range(len(temp) - 1):
                nt += rules[temp[i: i+2]]
            temp = nt + temp[-1]

        # Store results for faster expansion later and to keep track of counts after 20 iterations
        rules_expansion[r] = temp[:-1]
        counts[r] = Counter(temp[:-1])

    # Keep track of where in execution
    print("Expanded rules")

    # Get template after 20 iterations
    new_template = ''
    for i in range(len(template) - 1):
        new_template += rules_expansion[template[i: i+2]]

    template = new_template + template[-1]
    print("Half template")

    # Get the total number of each pair at halfway
    count_doubles = Counter(template[i: i+2] for i in range(len(template) - 1))
    total = defaultdict(int)

    # Off by one error correction
    total[template[-1]] = 1

    # Sum the total number of characters
    for doub, n in count_doubles.items():
        # print(doub, counts[doub])
        for char, count in counts[doub].items():
            total[char] += n * count

    # Return answer, total execution time on my machine: ~27 seconds
    return max(total.values()) - min(total.values())


f = read_file("./Input/Input14").split('\n\n')
p1(f)
p2(f)
