class SeaFloor:
    def __init__(self, x, y):
        self.floor = None
        self.shape = (x, y)

    @classmethod
    def from_file(cls, filename):
        floor = []
        with open(filename, "r") as file:
            for line in file:
                floor.append(list(line.strip()))
        seafloor = cls(len(floor[0]), len(floor))
        seafloor.floor = floor
        return seafloor

    def iterate(self, turn):
        if turn % 2 == 0:
            char, dx, dy = ">", 1, 0
        else:
            char, dx, dy = "v", 0, 1

        # print(f"Evaluating {char} cucumbers")

        copy = [["." for _ in line] for line in self.floor]

        for y, line in enumerate(self.floor):
            for x, cucumber in enumerate(line):

                if cucumber == ".":  # Skip empty positions
                    continue

                if cucumber != char:  # Not under consideration
                    copy[y][x] = cucumber
                    continue

                next_x = (x + dx) % self.shape[0]
                next_y = (y + dy) % self.shape[1]

                if self.floor[next_y][next_x] != ".":
                    copy[y][x] = cucumber
                    continue

                copy[y][x] = "."
                copy[next_y][next_x] = cucumber

        self.floor = copy

    def __repr__(self):
        return fmt(self.floor)


def fmt(floor):
    return "\n".join("".join(line) for line in floor)


def main():
    verbose = False
    floor = SeaFloor.from_file("./data.txt")

    if verbose:
        print(floor)

    n_turns = 1000
    previous = str(floor)
    broken = False
    for i in range(n_turns):
        floor.iterate(0)
        floor.iterate(1)
        if str(floor) == previous:
            broken = True
            print(f"Breaking at step: {i+1}!")
            break
        previous = str(floor)

        if (i + 1) % 10 == 0 and verbose:
            print(f"\n\n\n####### ITERATION {i+1} #######\n\n\n")
            print()
            print(floor)
            print()

    if not broken:
        print(f"Did not find solution in {n_turns} steps")


if __name__ == "__main__":
    main()
