import heapq
import math
from collections import defaultdict, deque

input_ = "./data.txt"
CARDS = [(-1,0), (1,0), (0,-1), (0,1)]

def man_dist(xs, ys, xe, ye):
    return abs(xe-xs) + abs(ye-ys)

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return not self.elements
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) :
        return heapq.heappop(self.elements)[1]


class Graph:
    
    def __init__(self):
        self.costs = []
        self.edges = defaultdict(list)
        self.path = set()
        self.my, self.mx = 0, 0

    @classmethod
    def from_file(cls, filename):
        graph = cls()
        with open(filename, "r") as file:
            for line in file:
                graph.costs.append([int(x) for x in line.strip()])
        graph.my = len(graph.costs)
        graph.mx = len(graph.costs[0])

        graph.init_edges()

        return graph

    def init_edges(self):
        for y, line in enumerate(self.costs):
            for x, _ in enumerate(line):
                for nx, ny in self.get_neighbors_coords(x,y):
                    self.edges[(x,y)].append((nx, ny))

    def get_neighbors_coords(self, x, y):
        for diff in CARDS:
            nx, ny = x+diff[0], y+diff[1]
            if nx < 0 or nx >= self.mx or ny < 0 or ny >= self.my:
                continue
            yield nx,ny

    def neighbors(self, coords):
        return self.edges[coords]

    def get_cost(self, x, y):
        return self.costs[y][x]

    def __repr__(self):
        s = []
        for y, line in enumerate(self.costs):
            l = []
            for x, cost in enumerate(line):
                if (x,y) in self.path:
                    l.append(f"({cost})")
                else:
                    l.append(f" {cost} ")
            s.append("".join(l))
        return "\n".join(s)


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.get_cost(*next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + man_dist(*next, *goal)
                frontier.put(next, priority)
                came_from[next] = current
    
    path = reconstruct_path(came_from, start, goal)
    return path, cost_so_far[goal]


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

def main():

    graph = Graph.from_file(input_)
    path, cost = a_star_search(graph, (0,0), (graph.mx-1, graph.my-1))
    for node in path:
        graph.path.add(node)

    print(graph)
    print(cost)

if __name__ == "__main__":
    main()
