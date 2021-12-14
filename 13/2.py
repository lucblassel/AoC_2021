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

    def write_ppm(self, filename):
        with open(filename, "w") as file:
            file.write("P3\n")
            file.write(f"{self.shape[0]} {self.shape[1]}\n")
            file.write("255\n")
            for line in self.dots:
                for val in line:
                    if val:
                        file.write("0 0 0\n")
                    else:
                        file.write("255 255 255\n")

    def __repr__(self):
        return "\n".join(
            ["".join(["#" if p else "." for p in line]) for line in self.dots]
        )

    def vertical_fold(self, fold_y):
        temp = [[v for v in l] for l in self.dots]
        for y in range(self.shape[1] - 1, fold_y, -1):
            y_new = 2 * fold_y - y
            for x, val in enumerate(self.dots[y]):
                temp[y_new][x] = val or self.dots[y_new][x]

        new_table = temp[:fold_y]

        self.dots = new_table
        self.shape = (self.shape[0], len(new_table))

    def horizontal_fold(self, fold_x):
        temp = [[v for v in l] for l in self.dots]
        for y, line in enumerate(self.dots):
            for x in range(self.shape[0] - 1, fold_x, -1):
                x_new = 2 * fold_x - x
                temp[y][x_new] = line[x] or line[x_new]
        new_table = [line[:fold_x] for line in temp]
        self.dots = new_table
        self.shape = (len(new_table[0]), self.shape[1])

    def count_dots(self):
        return sum(sum(line) for line in self.dots)


def main():
    paper = Paper.from_file(input_)
    paper.write_ppm("original.ppm")
    count = 1
    for fold_dir, fold_coord in paper.folds:
        if fold_dir == "y":
            paper.vertical_fold(fold_coord)
        else:
            paper.horizontal_fold(fold_coord)
        paper.write_ppm(f"fold_{count}.ppm")
        count += 1

    print(paper)
    print(paper.count_dots())


if __name__ == "__main__":
    main()
