input_ = "./data.txt"


class Paper:
    def __init__(self, shape):
        self.dots = [[False for _ in range(shape[0])] for _ in range(shape[1])]
        self.shape = shape
        self.folds = []

    def set_point(self, x, y):
        self.dots[y][x] = True

    @classmethod
    def from_file(cls, filename):
        points = []
        folds = []
        max_x, max_y = 0, 0
        with open(filename, "r") as file:
            for line in file:
                if line.strip() == "":
                    continue
                if line[:4] == "fold":
                    axis, coord = line.strip()[11:].split("=")
                    folds.append((axis, int(coord)))
                else:
                    x_s, y_s = line.strip().split(",")
                    x, y = int(x_s), int(y_s)
                    max_x, max_y = max(max_x, x), max(max_y, y)
                    points.append((x, y))
        paper = cls((max_x + 1, max_y + 1))
        for point in points:
            paper.set_point(*point)
        paper.folds = folds
        return paper

    def __repr__(self):
        return "\n".join(
            ["".join(["#" if p else "." for p in line]) for line in self.dots]
        )

    def vertical_fold(self, fold_y):
        new_table = []
        for y in range(self.shape[1] - 1, fold_y, -1):
            y_new = 2 * fold_y - y
            new_table.append(
                [val or self.dots[y_new][x] for x, val in enumerate(self.dots[y])]
            )
        self.dots = new_table
        self.shape = (self.shape[0], len(new_table))

    def horizontal_fold(self, fold_x):
        new_table = []
        for y, line in enumerate(self.dots):
            new_table.append([])
            for x in range(self.shape[0] - 1, fold_x, -1):
                new_table[-1].append(line[x] or line[2 * fold_x - x])
        self.dots = new_table
        self.shape = (len(new_table[0]), self.shape[1])

    def count_dots(self):
        return sum(sum(line) for line in self.dots)


def main():
    paper = Paper.from_file(input_)
    print(paper)
    print(paper.shape, paper.folds)
    print()
    fold_dir, fold_coord = paper.folds[0]
    if fold_dir == "y":
        paper.vertical_fold(fold_coord)
    else:
        paper.horizontal_fold(fold_coord)
    print(paper)
    print(paper.count_dots())


if __name__ == "__main__":
    main()
