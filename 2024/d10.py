from aocd import get_data
import collections


def is_valid(x, y, G):
    if x >= 0 and x < len(G) and y >= 0 and y < len(G[0]):
        return True
    return False


def dfs_trail(x, y, G, summits):
    val = int(G[x][y])
    if val == 9:
        summits[(x, y)] += 1
        return

    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx = x + dx
        ny = y + dy
        if is_valid(nx, ny, G) and int(G[nx][ny]) == val + 1:
            dfs_trail(nx, ny, G, summits)


def solver(G, fn):
    total = 0
    for x, row in enumerate(G):
        for y, col in enumerate(row):
            if col == '0':
                summits = collections.defaultdict(int)
                dfs_trail(x, y, G, summits)
                trails = fn(summits)
                total += trails
    return total


def part1(G):
    return solver(G, lambda summits: len(summits.keys()))


def part2(G):
    return solver(G, lambda summits: sum(summits.values()))


if __name__ == '__main__':
    data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
    data = get_data(year=2024, day=10)
    G = data.split('\n')

    print('part1', part1(G))
    print('part2', part2(G))
