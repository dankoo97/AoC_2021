from advent import read_file, timer
from itertools import product


def deterministic_die():
    while True:
        for i in range(1, 101):
            yield i


@timer
def p1(ins):
    players = [int(i[-1]) for i in ins]
    score = [0, 0]
    turn = False
    die = deterministic_die()
    cnt = 0

    while all(s < 1000 for s in score):
        players[int(turn)] = (players[int(turn)] + next(die) + next(die) + next(die)) % 10
        score[int(turn)] += players[int(turn)] if players[int(turn)] else 10
        turn = not turn
        cnt += 3

    return cnt * min(score)


@timer
def p2(ins):
    def take_turn(players, score, turn):
        if any(s >= 21 for s in score):
            # Kept getting syntax errors for using *iterable, unsure why...
            outcomes[players[0], players[1], score[0], score[1], turn] = int(turn), int(not turn)
            return outcomes[players[0], players[1], score[0], score[1], turn]

        if (players[0], players[1], score[0], score[1], turn) in outcomes:
            return outcomes[players[0], players[1], score[0], score[1], turn]

        player1 = 0
        player2 = 0
        for a, b, c in product((1, 2, 3), repeat=3):
            roll = a + b + c
            np = [p for p in players]
            np[int(turn)] = (np[int(turn)] + roll) % 10

            ns = [s for s in score]
            ns[int(turn)] += np[int(turn)] if np[int(turn)] else 10

            universes = take_turn(np, ns, not turn)
            player1 += universes[0]
            player2 += universes[1]

        outcomes[(*players, *score, turn)] = player1, player2
        return player1, player2

    outcomes = {}
    m = take_turn(tuple(int(i[-1]) for i in ins), (0, 0), False)

    return max(m)


f = read_file("./Input/Input21").split('\n')
p1(f)
p2(f)
