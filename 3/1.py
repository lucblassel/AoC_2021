from collections import Counter

input_ = "./data.txt"

def getMostCommon(filename):
    columns = None
    with open(input_, "r") as file:
        for tot, line in enumerate(file):
            l = line.strip()
            if columns is None:
                columns = [""] * len(l)
            for i, char in enumerate(l):
                columns[i] += char
    counters = [Counter(l) for l in columns]
    return [
        int(c['1'] > tot/2)
        for c in counters
    ]


def to_decimal(bits):
    return int(
        "".join(str(b) for b in bits), 2
    )

def main():
    gamma = getMostCommon(input_)
    epsilon = [1-x for x in gamma]

    print(to_decimal(epsilon) * to_decimal(gamma))

if __name__ == "__main__":
    main()
