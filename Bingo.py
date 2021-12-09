from advent import read_file, timer


def check_winner(b):
    # Check for winning rows and columns
    for r in range(5):
        if all(c[1] for c in b[r]):
            return True
        if all(b[i][r][1] for i in range(5)):
            return True
    return False


def mark(b, c):
    # Check each cell for number c and mark if called
    for i in range(5):
        for j in range(5):
            if b[i][j][0] == c:
                b[i][j] = (c, True)


def unmarked(b):
    # Gather all unmarked into a list
    s = []
    for i in range(5):
        for j in range(5):
            if not b[i][j][1]:
                s.append((b[i][j][0]))

    return s


def create_board(ins):
    b = []
    for r in ins.split('\n'):
        # Create a row with the number and a called mark
        b.append([(int(i), False) for i in r.split()])

    return b


@timer
def p1(ins):
    called = tuple(int(i) for i in ins[0].split(','))
    boards = []

    for b in ins[1:]:
        boards.append(create_board(b))

    winner = None
    last = None

    for c in called:
        if winner:
            break

        for b in boards:
            mark(b, c)
            if check_winner(b):
                winner = b
                last = c

    s = unmarked(winner)

    return last * sum(s)


@timer
def p2(ins):
    # Create called numbers list and boards
    called = tuple(int(i) for i in ins[0].split(','))
    boards = []
    for b in ins[1:]:
        boards.append(create_board(b))

    # Create a list of won boards, used to skip won boards
    won = [False] * len(boards)

    # Track last winner and last number called
    winner = None
    last = None

    # Iterate through called numbers
    for c in called:

        # If all boards have won, stop calling
        if all(won):
            break

        # Iterate through the boards
        for i, b in enumerate(boards):

            # Skip won boards
            if won[i]:
                continue

            # Mark called number
            mark(b, c)

            # Check if board won after calling and mark winner
            if check_winner(b):
                won[i] = True
                winner = b

        # Store last number
        last = c

    # Get a list of unmarked in the last winner
    s = unmarked(winner)

    # DEBUG
    # print(winner)
    # print(sum(s))
    # print(last)

    # Puzzle Answer
    return last * sum(s)


f = read_file("./Input/Input04").split('\n\n')
p1(f)
p2(f)
