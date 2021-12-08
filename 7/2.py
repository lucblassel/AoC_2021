from statistics import mean

input_ = "./data.txt"


def compute_fuel_usage(positions, destination):  # cost function
    fuel = 0
    for position in positions:
        fuel += (destination - position) ** 2 + abs(destination - position)
    return fuel // 2

def main():
    with open(input_, "r") as in_:
        positions = [int(x) for x in in_.readlines()[0].split(",")]

    opt = int(mean(positions))
    candidates = [opt - 1, opt, opt + 1]

    f = -1
    d = 0
    for candidate in candidates:
        f_c = compute_fuel_usage(positions, candidate)
        if f_c < f or f < 0:
            f = f_c
            d = candidate

    print(f, d, mean(positions))


if __name__ == "__main__":
    main()
