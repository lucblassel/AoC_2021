from collections import defaultdict, Counter
from string import ascii_uppercase

input_ = "./data.txt"


def copy_defaultdict(d):
    d_c = defaultdict(int)
    for k, v in d.items():
        d_c[k] = v
    return d_c


def traverse(start, graph, visited, path):
    count = 0
    path.append(start)
    if start == "end":
        return 1
    if start.upper() != start:
        visited[start] += 1
    for node in graph[start]:
        counts = Counter(visited.values())
        if visited[start] <= 2 and node != "start" and counts[2] < 2:
            v = copy_defaultdict(visited)
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

    count = traverse("start", graph, defaultdict(int), [])
    print(count)
    print(dict(graph))


if __name__ == "__main__":
    main()
