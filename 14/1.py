from collections import defaultdict, Counter

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


def apply_step(seq, operators):
    new_seq = seq[0]
    for i in range(len(seq) - 1):
        new_seq += operators.get(seq[i : i + 2], "") + seq[i + 1]
    return new_seq


def main():
    seq, operators = parse_input(input_)
    new_seq = seq
    for i in range(10):
        new_seq = apply_step(new_seq, operators)

    counts = Counter(new_seq)
    print(max(counts.values()) - min(counts.values()))


if __name__ == "__main__":
    main()
