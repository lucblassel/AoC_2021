from collections import defaultdict
from string import ascii_uppercase

input_ = "./data.txt"


def traverse(start, graph, visited, path):
    count = 0
    path.append(start)
    if start == "end":
        return 1
    if start.upper() != start:
        visited.add(start)
    for node in graph[start]:
        if node not in visited:
            v = set(x for x in visited)
            p = [x for x in path]
            count += traverse(node, graph, v, p)
    return count


def main():
    graph = defaultdict(list)
    with open(input_, "r") as file:
        for line in file:
            n1, n2 = line.strip().split("-")
            graph[n1].append(n2)
            graph[n2].append(n1)

    count = traverse("start", graph, {"start"}, [])
    print(count)


if __name__ == "__main__":
    main()
