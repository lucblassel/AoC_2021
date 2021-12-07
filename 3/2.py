from collections import Counter
import array

input_ = "./data.txt"


class BitTable:
    parser = {"1": 1, "0": 0}

    def __init__(self):
        self.table = []
        self.shape = (0, 0)

    @staticmethod
    def _parse_line(line):
        return array.array("b", [BitTable.parser.get(x) for x in line.strip()])

    @classmethod
    def from_file(cls, filename):
        table = cls()
        with open(filename, "r") as lines:
            for index, line in enumerate(lines):
                table.table.append(cls._parse_line(line))
        table._set_shape()
        return table

    def _set_shape(self):
        self.shape = (len(self.table), len(self.table[0]))

    def getMostCommonValue(self, index):
        return int(sum(x[index] for x in self.table) >= self.shape[0] / 2)

    def filter(self, index, val):
        other = BitTable()
        for line in self.table:
            if line[index] == val:
                other.table.append(line)
        other._set_shape()
        return other

    def __repr__(self):
        return "\n".join(str(x.tolist()) for x in self.table) + f" {self.shape}"

    def getNum(self, index=0):
        return self.to_decimal(self.table[index])

    @staticmethod
    def to_decimal(bits):
        return int("".join(str(b) for b in bits), 2)


def applyFilters(table, start_index, least=False):
    i = start_index

    while table.shape[0] > 1:
        c = table.getMostCommonValue(i)
        if least:
            c = 1 - c
        table = table.filter(i, c)
        i = (i + 1) % table.shape[1]

    return table


def main():
    bt = BitTable.from_file(input_)
    c = bt.getMostCommonValue(0)
    s1, s2 = bt.filter(0, c), bt.filter(0, 1 - c)
    oxygen = applyFilters(s1, 1)
    co2 = applyFilters(s2, 1, True)

    o, c = oxygen.getNum(), co2.getNum()
    print(o, c, o * c)


if __name__ == "__main__":
    main()
