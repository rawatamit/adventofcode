from aocd import get_data
import collections


def get_start(G):
    for r in range(len(G)):
        for c in range(len(G[r])):
            if G[r][c] == 'S':
                return r, c
    return -1, -1


def is_valid(G, r, c):
    rows = len(G)
    cols = len(G[0])
    if r < 0 or r >= rows:
        return False
    if c < 0 or c >= cols:
        return False
    return True


def is_ht_diff_valid(old_height, new_height):
    # E is the ending position
    clean_new_height = 'z' if new_height == 'E' else new_height
    return ord(clean_new_height) <= ord(old_height) + 1


def search(G, sr, sc):
    dr = [-1, 0, 0, 1]
    dc = [0, -1, 1, 0]

    Q = collections.deque()
    Q.append((sr, sc, 'a', 0))

    seen = set()
    seen.add((sr, sc))

    while Q:
        r, c, height, steps = Q.popleft()
        if height == 'E':
            return steps
        for i in range(len(dr)):
            nr = r + dr[i]
            nc = c + dc[i]
            if (is_valid(G, nr, nc) and
                is_ht_diff_valid(height, G[nr][nc]) and
                not (nr, nc) in seen):
                seen.add((nr, nc))
                Q.append((nr, nc, G[nr][nc], steps+1))
    return -1


if __name__ == '__main__':
    data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    data = get_data(year=2022, day=12)
    G = data.split('\n')
    sr, sc = get_start(G)
    steps = search(G, sr, sc)
    print('part1', steps)

    minsteps = len(G) * len(G[0])
    for r in range(len(G)):
        for c in range(len(G[r])):
            if G[r][c] in ('S', 'a'):
                sr, sc = r, c
                steps = search(G, sr, sc)
                if steps != -1:
                    minsteps = min(steps, minsteps)
    print('part2', minsteps)

