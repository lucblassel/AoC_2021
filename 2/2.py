input_ = "./data.txt"


class Submarine:

    _dirs = {
        "up": -1,
        "down": 1,
    }

    def __init__(self, x=0, y=0, aim=0):
        self.x = x
        self.y = y
        self.aim = 0

    def _move_y(self, y):
        self.y += y

    def _move_x(self, x):
        self.x += x

    def _change_aim(self, aim):
        self.aim += aim

    def move(self, direction, amount):
        if direction == "forward":
            self._move_x(amount)
            self._move_y(amount * self.aim)
        else:
            self._change_aim(amount * Submarine._dirs.get(direction, 0))

    def print_pos(self):
        print(f"X: {self.x}, Y:{self.y} (prod: {self.x * self.y})")


def parseline(line):
    direction, amount = line.strip().split()
    return direction, int(amount)


def main():
    sub = Submarine()

    with open(input_, "r") as lines:
        for line in lines:
            direction, amount = parseline(line)
            sub.move(direction, amount)

    sub.print_pos()


if __name__ == "__main__":
    main()
