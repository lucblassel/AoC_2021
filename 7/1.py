from statistics import median

input_ = "./data.txt"


def compute_fuel_usage(positions, destination):
    fuel = 0
    for position in positions:
        fuel += abs(position - destination)
    return fuel


def main():
    with open(input_, "r") as in_:
        positions = [int(x) for x in in_.readlines()[0].split(",")]
    m = int(median(positions))
    f = compute_fuel_usage(positions, m)
    print(m, f)


if __name__ == "__main__":
    main()
