input_ = "./data.txt"

class SeaFloor:
    def __init__(self, x, y):
        self.shape = (x, y)
        self.octopi = []
        self.flashed= []
        self.flashes = 0

    @classmethod
    def from_file(cls, filename):
        t = []
        with open(filename, "r") as file:
            for line in file:
                t.append(
                    [int(x) for x in line.strip()]
                )
        floor = cls(len(t), len(t[0]))
        floor.octopi = t
        floor.reset_flashed()
        return floor

    def reset_flashed(self):
        self.flashed = [
            [False for _ in range(self.shape[1])]
            for _ in range(self.shape[0])
        ]

    def __repr__(self):
        s = []
        for line in self.octopi:
            l = []
            for char in line:
                if char == 0:
                    l.append(f"({char})")
                else:
                    l.append(f" {char} ")
            s.append("".join(l))
        return "\n".join(s)

    def iterate_neighbors(self, x, y):
        for i in range(x-1, x + 2):
            for j in range(y - 1, y + 2):
                if i == x and j == y:
                    continue
                if i < 0 or i >= self.shape[0] or j < 0 or j >= self.shape[1]:
                    continue
                yield i, j

    def flash(self, x, y):
        self.flashed[x][y] = True
        self.flashes += 1
        for i,j in self.iterate_neighbors(x, y):
            self.octopi[i][j] += 1
            if self.octopi[i][j] > 9 and not self.flashed[i][j]:
                self.flash(i,j)

    def process_iteration(self):
        for i, line in enumerate(self.octopi):
            for j, val in enumerate(line):
                self.octopi[i][j] += 1
        for i, line in enumerate(self.octopi):
            for j,val in enumerate(line):
                if val > 9 and not self.flashed[i][j]:
                    self.flash(i,j)
        if self.check_all_flashed():
            return True
        for i, line in enumerate(self.flashed):
            for j, flashed in enumerate(line):
                if flashed:
                    self.octopi[i][j] = 0
                    self.flashed[i][j] = False

    def check_all_flashed(self):
        for line in self.flashed:
            for flashed in line:
                if not flashed:
                    return False
        return True

def main():
    floor = SeaFloor.from_file(input_)
    counter = 1
    while True:
        all_flashed = floor.process_iteration()
        if all_flashed:
            break
        counter += 1
    print(floor, counter)


if __name__ =="__main__":
    main()
