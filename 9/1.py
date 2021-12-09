
input_ = "./data.txt"

class HeatMap:

    def __init__(self):
        self.map = []
        self.checked = []
        self.lowpoints = []
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

    def find_lowpoints(self):
        for i_curr, line in enumerate(self.map):
            for j_curr, val in enumerate(line):
                if self.checked[i_curr][j_curr] is not None:
                    continue
                smallest = True
                for i_neighb, j_neighb, val_neighb in self.iterate_neighbors(i_curr, j_curr):
                    if val_neighb <= val:
                        smallest = False
                        continue
                    self.checked[i_neighb][j_neighb] = False
                if smallest:
                    self.checked[i_curr][j_curr] = True
                    self.lowpoints.append(val)

def main():
    heatmap = HeatMap.from_file(input_)
    heatmap.find_lowpoints()
    print(heatmap)
    print(heatmap.lowpoints, sum(heatmap.lowpoints) + len(heatmap.lowpoints))


if __name__ == "__main__":
    main()
