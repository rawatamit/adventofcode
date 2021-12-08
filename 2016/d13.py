from collections import deque
from aocd.models import Puzzle


def is_open(x, y, favnum):
    tmp = x*x + 3*x + 2*x*y + y + y*y
    return len([x for x in bin(tmp + favnum)
                    if x == '1']) % 2 == 0


def neigbors(x, y):
    dxs = [1, -1, 0, 0]
    dys = [0, 0, 1, -1]
    for i, dx in enumerate(dxs):
        nx = x + dx
        ny = y + dys[i]

        if 0 <= nx and 0 <= ny:
            yield nx, ny


def bfs(favnum, dest, max_steps=-1):
    Q = deque()
    Q.append(((1, 1), 0))
    seen = set()

    while Q:
        u, steps = Q.popleft()
        x, y = u

        # found destination
        if max_steps == -1 and u == dest:
            return steps

        # only exploring
        if max_steps != -1 and steps > max_steps:
            continue

        seen.add(u)

        for v in neigbors(x, y):
            nx, ny = v
            if v not in seen and is_open(nx, ny, favnum):
                Q.append((v, steps + 1))
    
    return len(seen)


if __name__ == '__main__':
    puzzle = Puzzle(year=2016, day=13)
    favnum = int(puzzle.input_data)

    assert is_open(1,1,10)
    assert not is_open(1,0,10)

    print(bfs(favnum, (31, 39)))
    print(bfs(favnum, None, max_steps=50))
