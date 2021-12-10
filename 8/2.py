from collections import defaultdict
from itertools import product

input_ = "./data.txt"

NUMBERS = [
    {0, 1, 2, 4, 5, 6},
    {2, 5},
    {0, 2, 3, 4, 6},
    {0, 2, 3, 5, 6},
    {1, 2, 3, 5},
    {0, 1, 3, 5, 6},
    {0, 1, 3, 4, 5, 6},
    {0, 2, 5},
    {0, 1, 2, 3, 4, 5, 6},
    {0, 1, 2, 3, 5, 6},
]


def sort_word(string):
    return "".join(sorted(string))


def get_lengths(patterns):
    lengths = defaultdict(list)
    for pattern in patterns:
        lengths[len(pattern)].append(sort_word(pattern))
    return lengths


def find_unique_segments(lengths):
    segments = dict()
    pairs = [[], [], [], []]
    for letter in lengths[2][0]:
        segments[letter] = {2, 5}
        pairs[0].append(letter)
    for letter in lengths[3][0]:
        if letter not in segments:
            segments[letter] = {0}
            pairs[1].append(letter)
    for letter in lengths[4][0]:
        if letter not in segments:
            segments[letter] = {1, 3}
            pairs[2].append(letter)
    for letter in lengths[7][0]:
        if letter not in segments:
            segments[letter] = {4, 6}
            pairs[3].append(letter)
    return segments, pairs


def get_segment_iterator(singletons):
    if len(singletons) == 1:
        return ({s} for s in singletons[0])
    return (set(s) for s in product(*singletons))


def resolve_number(pattern, segments, pairs):
    lit_up = set()
    singletons = list()

    for pair in pairs:
        if sum(elem in pattern for elem in pair) != len(pair):
            singletons.append(segments[pair[0]])
            continue
        lit_up.update(segments[pair[0]])

    for candidate in get_segment_iterator(singletons):
        candidate_lit_up = lit_up.union(candidate)
        if candidate_lit_up in NUMBERS:
            return NUMBERS.index(candidate_lit_up)


def get_numbers(patterns):

    lengths = get_lengths(patterns)
    segments, pairs = find_unique_segments(lengths)

    resolved = {lengths[2][0]: 1, lengths[4][0]: 4, lengths[3][0]: 7, lengths[7][0]: 8}

    for l in [5, 6]:
        for pattern in lengths[l]:
            n = resolve_number(pattern, segments, pairs)
            if n is not None:
                resolved[pattern] = n

    return resolved


def digits_to_number(digits):
    total = 0
    for pw, digit in enumerate(digits[::-1]):
        total += digit * (10 ** pw)
    return total


def main():
    total = 0

    with open(input_, "r") as file:
        for line in file:
            p, o = line.strip().split(" | ")
            patterns, outputs = p.split(" "), o.split(" ")
            resolved = get_numbers(patterns)
            digits = [resolved.get(sort_word(x)) for x in outputs]
            solution = digits_to_number(digits)
            total += solution

    print("\n", total)


if __name__ == "__main__":
    main()
