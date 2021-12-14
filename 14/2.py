from collections import defaultdict, Counter
from copy import copy

input_ = "./data.txt"


def parse_input(filename):
    with open(input_, "r") as file:
        seq = file.__next__().strip()
        operators = dict()
        for line in file:
            if line.strip() == "":
                continue
            pair, ins = line.strip().split(" -> ")
            operators[pair] = ins

    return seq, operators


def get_counts(seq):
    counts, pair_counts = defaultdict(int), defaultdict(int)
    for i in range(len(seq) - 1):
        pair_counts[seq[i : i + 2]] += 1
        counts[seq[i]] += 1
    counts[seq[-1]] += 1
    return counts, pair_counts


def main():
    seq, operators = parse_input(input_)

    counts, pair_counts = get_counts(seq)

    for i in range(40):
        new_dict = defaultdict(int)
        for pair, n_pair in pair_counts.items():
            ins = operators[pair]
            new_dict[pair[0] + ins] += n_pair
            new_dict[ins + pair[1]] += n_pair
            counts[ins] += n_pair
        pair_counts = new_dict

    print(max(counts.values()) - min(counts.values()))


if __name__ == "__main__":
    main()
