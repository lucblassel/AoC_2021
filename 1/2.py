input_ = "./data.txt"

def main():
    n = 0
    elems = []

    with open(input_, "r") as infile:
        for i, line in enumerate(infile):
            measure = int(line.strip())
            if len(elems) < 4:
                elems.append(measure)
                continue
            if sum(elems[:-1]) < sum(elems[1:]):
                n += 1
            elems = elems[1:] + [measure]
    if sum(elems[:-1]) < sum(elems[1:]):
        n += 1
    print(n)


if __name__ == "__main__":
    main()
