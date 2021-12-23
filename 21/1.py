from itertools import cycle


def get_score(roll):
    return (roll - 1) % 10 + 1


def main():
    die = cycle(range(1, 101))
    # start = [4, 8] # Test input
    start = [4, 7]  # Real input
    scores = [0, 0]
    nrounds = 0
    finished = False

    while not finished:
        for player, pos in enumerate(start):
            rolls = 0
            for _ in range(3):
                roll = die.__next__()
                rolls += roll
            space = get_score(pos + rolls)
            start[player] = space
            scores[player] += space
            nrounds += 1

            if max(scores) >= 1000:
                finished = True
                break

    print(min(scores) * nrounds * 3)


if __name__ == "__main__":
    main()
