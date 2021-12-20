from aocd.models import Puzzle
from heapq import heappop, heappush
from collections import defaultdict
from itertools import permutations


def dijkstra(G, start, end):
    Q = [(0, start)]
    D = {start: 0}

    while Q:
        dist_start, u = heappop(Q)
        if u == end: return dist_start

        for v, wt in G[u]:
            cur_dist = D.get(v, float('inf'))

            if v not in D and wt + D[u] < cur_dist:
                D[v] = wt + D[u]
                heappush(Q, (D[v], v))

    return -1


if __name__ == '__main__':
    puzzle = Puzzle(year=2015, day=9)

    data = '''London to Dublin = 464
              London to Belfast = 518
              Dublin to Belfast = 141'''
    
    data = puzzle.input_data
    
    G = defaultdict(list)

    for line in data.split('\n'):
        u, vwt = line.strip().split('to')
        v, wt = vwt.split('=')

        u, v, wt = u.strip(), v.strip(), int(wt)

        G[u].append((v, wt))
        G[v].append((u, wt))

    assp = defaultdict(dict)

    for start in G.keys():
        for end in G.keys():
            if start != end:
                assp[start][end] = dijkstra(G, start, end)
    
    minpathsum = float('inf')
    maxpathsum = -float('inf')

    for perm in permutations(G.keys(), len(G.keys())):
        pathsum = sum(assp[perm[i-1]][perm[i]]
                        for i in range(1, len(perm)))
        minpathsum = min(minpathsum, pathsum)
        maxpathsum = max(maxpathsum, pathsum)
    
    print(minpathsum, maxpathsum)
