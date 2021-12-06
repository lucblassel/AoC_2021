input_ = "./data.txt"

def main():
    n = 0
    prev = None
    with open(input_, "r") as infile:
        for i, line in enumerate(infile):
            measure = int(line.strip())
            if i > 0 and measure > prev:
                n += 1
            prev = measure
    print(n)


if __name__ == "__main__":
    main()
