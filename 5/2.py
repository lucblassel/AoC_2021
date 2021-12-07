import array

input_ = "./data.txt"


def inf_gen(val):
    while True:
        yield val


class Line:
    def __init__(self, x1, y1, x2, y2, orient):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.orient = orient

    @classmethod
    def from_string(cls, string):
        (x1, y1), (x2, y2) = [
            [int(x) for x in seg.split(",")] for seg in string.split(" -> ")
        ]

        if x1 != x2 and y1 != y2:
            orient = "diagonal"
        elif x1 != x2 and y1 == y2:
            orient = "horizontal"
        else:
            orient = "vertical"

        return cls(x1, y1, x2, y2, orient)

    def __repr__(self):
        return f"({self.x1},{self.y1})->({self.x2},{self.y2}) ({self.orient[0]})"

    def traverse(self):
        if self.orient == "horizontal":
            x_it = range(min(self.x1, self.x2), max(self.x1, self.x2) + 1)
            y_it = inf_gen(self.y1)
        elif self.orient == "vertical":
            x_it = inf_gen(self.x1)
            y_it = range(min(self.y1, self.y2), max(self.y1, self.y2) + 1)
        else:
            if self.x1 > self.x2:
                x_it = range(self.x1, self.x2 - 1, -1)
            else:
                x_it = range(self.x1, self.x2 + 1)

            if self.y1 > self.y2:
                y_it = range(self.y1, self.y2 - 1, -1)
            else:
                y_it = range(self.y1, self.y2 + 1)

        for x, y in zip(x_it, y_it):
            yield x, y


class Floor:
    def __init__(self, size_x, size_y):
        self.floor = [
            array.array("B", [0 for _ in range(size_x)]) for _ in range(size_y)
        ]

    def __repr__(self):
        return "\n".join(
            " ".join(str(x) if x != 0 else "." for x in line) for line in self.floor
        )

    def add_vent(self, x, y):
        self.floor[y][x] += 1

    def count_greater(self, threshold):
        count = 0
        for row in self.floor:
            for value in row:
                if value > threshold:
                    count += 1
        return count


def main():
    max_x, max_y = 0, 0
    lines = []
    with open(input_, "r") as f_lines:
        for f_line in f_lines:
            line = Line.from_string(f_line.strip())
            lines.append(line)
            max_x = max(max_x, max(line.x1, line.x2))
            max_y = max(max_y, max(line.y1, line.y2))
    floor = Floor(max_x + 1, max_y + 1)

    for line in lines:
        for x, y in line.traverse():
            floor.add_vent(x, y)

    print(floor.count_greater(1))


if __name__ == "__main__":
    main()
