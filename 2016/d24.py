from aocd.models import Puzzle
from collections import deque
from collections import defaultdict
from itertools import permutations


def find_locations(grid):
    locs = {grid[y][x]: (x, y)
            for y in range(len(grid))
            for x in range(len(grid[0]))
            if grid[y][x].isdigit()}
    return locs


def neighbors(grid, u):
    dxs = [0, 0, -1, +1]
    dys = [1, -1, 0, 0]

    x, y = u
    for i, dx in enumerate(dxs):
        nx = x + dx
        ny = y + dys[i]

        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            yield nx, ny


def bfs(grid, start, end):
    Q = deque([(start, 0)])
    seen = set([start])

    while Q:
        u, steps = Q.pop()
        if u == end: return steps

        for v in neighbors(grid, u):
            nx, ny = v
            if v not in seen and grid[ny][nx] != '#':
                seen.add(v)
                Q.appendleft((v, steps + 1))
    
    return -1


def tsp(grid):
    locs = find_locations(grid)
    all_shortest = defaultdict(dict)

    for achar, aloc in locs.items():
        for bchar, bloc in locs.items():
            if achar != bchar:
                min_dist = bfs(grid, aloc, bloc)
                all_shortest[aloc][bloc] = min_dist
                all_shortest[bloc][aloc] = min_dist
    
    # we always start at 0, and shouldn't appear in the permutations
    digit_locs = [loc for x, loc in locs.items() if x != '0']

    part1 = float('inf')
    part2 = float('inf')

    for path in permutations(digit_locs):
        cur = locs['0']
        tsum = 0
        for x in path:
            tsum += all_shortest[cur][x]
            cur = x
        part1 = min(part1, tsum)
        part2 = min(part2, tsum + all_shortest[path[-1]][locs['0']])
    return part1, part2


if __name__ == '__main__':
    puzzle = Puzzle(year=2016, day=24)
    data = puzzle.input_data

    grid = [
        '###########',
        '#0.1.....2#',
        '#.#######.#',
        '#4.......3#',
        '###########']
    
    grid = data.split('\n')

    print(tsp(grid))
