from collections import defaultdict
from collections import Counter
from aocd.models import Puzzle


class Graph:
    def __init__(self) -> None:
        self.edges = defaultdict(list)
    
    def __str__(self) -> str:
        return f'Graph<{self.edges}>'
    
    def add_edge(self, u, v):
        self.edges[u].append(v)
        self.edges[v].append(u)
    
    def get_edges(self, u):
        return self.edges[u]


def is_big_cave(u):
    return u.isupper()


def is_small_cave(u):
    return u.islower()


def can_add_to_path(v, path):
    if is_big_cave(v): return True
    # v is not any of the small caves in path
    return v not in set(x for x in path if is_small_cave(x))


def can_add_to_path_part2(v, path):
    if is_big_cave(v): return True
    if v == 'start' and v in path: return False
    if v == 'end' and v in path: return False

    count = Counter(x for x in path if is_small_cave(x))
    # most frequent vertex in path
    most_freq = count.most_common()[0][1]

    # if vertex v is not in path, allow max two of other vertices
    if v not in count: return most_freq <= 2
    
    # if vertex v is in path, only allow one copy of any other vertex
    return count[v] <= 1 and count.most_common()[0][1] <= 1


def search(G, start, end, can_add_fn=can_add_to_path):
    Q = [[start]]

    while Q:
        path = Q.pop()
        u = path[-1]

        if u == end:
            # path ends at end
            yield path
        else:
            for v in G.get_edges(u):
                if can_add_fn(v, path):
                    path_new = path + [v]
                    Q.append(path_new)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=12)

    data = '''start-A
              start-b
              A-c
              A-b
              b-d
              A-end
              b-end'''

    data = puzzle.input_data

    G = Graph()
    for line in data.split('\n'):
        u, v = line.strip().split('-')
        G.add_edge(u, v)
    
    # part 1
    paths = search(G, 'start', 'end')
    print(len(list(paths)))

    # part 2
    paths = search(G, 'start', 'end', can_add_fn=can_add_to_path_part2)
    print(len(list(paths)))
