from functools import reduce

input_ = "./data.txt"

class HeatMap:

    def __init__(self):
        self.map = []
        self.checked = []
        self.basins = []
        self.shape = None

    @classmethod
    def from_file(cls, filename):
        heatmap = HeatMap()
        with open(filename, "r") as file:
            for line in file:
                heatmap.map.append(
                    [int(x) for x in line.strip()]
                )
                heatmap.checked.append([None for _ in line.strip()])
        heatmap.shape = (len(heatmap.map), len(heatmap.map[0]))
        return heatmap

    def __repr__(self):
        return "\n".join(
            "".join(
                f"({x})" if self.checked[i][j] else f" {x} "
                for j,x in enumerate(line)
            )
            for i, line in enumerate(self.map)
        )

    def iterate_neighbors(self, i_curr, j_curr):
        dirs = [(-1,0), (1,0), (0,-1), (0,1)]
        for x_inc, y_inc in dirs:
            i, j = i_curr + x_inc, j_curr + y_inc
            if i < 0 or i >= self.shape[0] or j < 0 or j >= self.shape[1]:
                continue
            yield i, j, self.map[i][j]


    def find_basin(self, seed_i, seed_j):
        stack = [(seed_i, seed_j)]
        self.basins.append([self.map[seed_i][seed_j]])
        self.checked[seed_i][seed_j] = True
        while len(stack) > 0:
            i_curr, j_curr = stack.pop()
            for i, j, val in self.iterate_neighbors(i_curr, j_curr):
                if val != 9 and self.checked[i][j] is None:
                    stack.append((i,j))
                    self.basins[-1].append(val)
                self.checked[i][j] = val != 9

    def find_basins(self):
        for i, line in enumerate(self.map):
            for j, val in enumerate(line):
                if self.checked[i][j] is None and val != 9:
                    self.find_basin(i, j)

def main():
    heatmap = HeatMap.from_file(input_)
    heatmap.find_basins()
    print(heatmap)
    print()
    solution = reduce(lambda x1, x2: x1 * x2, sorted([len(x) for x in heatmap.basins])[-3:])
    print(solution)

if __name__ == "__main__":
    main()
