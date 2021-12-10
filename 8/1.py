from collections import defaultdict

input_ = "./data.txt"

uniques = {2: 1, 4: 4, 3: 7, 7: 8}


def main():
    patterns, outputs = [], []
    counter = defaultdict(int)

    with open(input_, "r") as file:
        for line in file:
            p, o = line.strip().split(" | ")
            patterns.append(p.split(" "))
            outputs.append(o.split(" "))

    for pattern in outputs:
        for signal in pattern:
            for l, v in uniques.items():
                if len(signal) == l:
                    print(signal, v)
                    counter[v] += 1

    print(sum(counter.values()))


if __name__ == "__main__":
    main()
