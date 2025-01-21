from aocd import get_data


def is_edge(G, r, c):
    rows = len(G[0])
    cols = len(G)
    if r == 0 or r == (rows - 1):
        return True
    if c == 0 or c == (cols - 1):
        return True
    return False


def is_valid(G, r, c):
    rows = len(G[0])
    cols = len(G)
    if r < 0 or r >= rows:
        return False
    if c < 0 or c >= cols:
        return False
    return True


def helper(G, r, c, dr, dc):
    oval = int(G[r][c])
    while not is_edge(G, r, c):
        nr = r + dr
        nc = c + dc
        if not is_valid(G, nr, nc):
            return False
        if int(G[nr][nc]) >= oval:
            return False
        r, c = nr, nc
    return True


def is_visible(G, r, c):
    return (helper(G, r, c, -1, 0) or
            helper(G, r, c, 0, -1) or
            helper(G, r, c, 0, 1) or
            helper(G, r, c, 1, 0))


def score(G, r, c, dr, dc):
    oval = int(G[r][c])
    nvisible = 0
    while not is_edge(G, r, c):
        nr = r + dr
        nc = c + dc
        if not is_valid(G, nr, nc):
            break
        nvisible += 1
        if int(G[nr][nc]) >= oval:
            break
        r, c = nr, nc
    return nvisible


def scenic_score(G, r, c):
    return (score(G, r, c, -1, 0) *
            score(G, r, c, 0, -1) *
            score(G, r, c, 0, 1) *
            score(G, r, c, 1, 0))


if __name__ == '__main__':
    data = """30373
25512
65332
33549
35390"""
    data = get_data(year=2022, day=8)
    G = data.split('\n')
    totvis = 0
    for r in range(len(G)):
        for c in range(len(G[0])):
            if is_visible(G, r, c):
                totvis += 1

    print('part1', totvis)

    maxscore = 0
    for r in range(len(G)):
        for c in range(len(G[0])):
            maxscore = max(maxscore, scenic_score(G, r, c))
    print('part 2', maxscore)

