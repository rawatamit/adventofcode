from aocd import get_data
from collections import deque


def get_pos(x, y, c):
    door_change = {'W': (0, -1), 'E': (0, +1), 'N': (-1, 0), 'S': (+1, 0)}
    pos_change = {'W': (0, -2), 'E': (0, +2), 'N': (-2, 0), 'S': (+2, 0)}
    pdx, pdy = pos_change[c]
    ddx, ddy = door_change[c]
    return (x + pdx, y + pdy), (x + ddx, y + ddy)


def trace_path(regex):
    pos_stack = []
    x, y = 0, 0
    path = {(x, y): 'X'}

    for c in regex:
        if c == '^' or c == '(':
            pos_stack.append((x, y))
        elif c == '$' or c == ')':
            pos_stack.pop()
        elif c == '|':
            # look at the previous position
            x, y = pos_stack[-1]
            # this is a door
            path[(x, y)] = '.'
        else: # a direction
            (x, y), (doorx, doory) = get_pos(x, y, c)
            # a room
            path[(x, y)] = '.'
            path[(doorx, doory)] = '|' if c in ('E', 'W') else '-'
    return path


def create_grid(path):
    cells = path.keys()
    min_x = min(cells, key=lambda k: k[0])[0] - 1
    max_x = max(cells, key=lambda k: k[0])[0] + 1
    min_y = min(cells, key=lambda k: k[1])[1] - 1
    max_y = max(cells, key=lambda k: k[1])[1] + 1
    grid = []
    for x in range(min_x, max_x + 1):
        row = []
        for y in range(min_y, max_y + 1):
            if (x, y) in path:
                row.append(path[(x, y)])
            else:
                row.append('#')
        grid.append(row)
    return grid


def print_grid(grid):
    for row in grid:
        print(''.join(row))


def enumerate_rooms(grid, start_x, start_y):
    nrows = len(grid)
    ncols = len(grid[0])
    q = deque()
    # position and number of steps from start
    q.append((start_x, start_y, 0))
    seen = set()
    seen.add((start_x, start_y))
    max_steps = -1
    atleast_1000 = 0

    while q:
        x, y, steps = q.popleft()

        # part 1
        if grid[x][y] == '.' and steps > max_steps:
            max_steps = steps
        
        # part 2
        if grid[x][y] == '.' and steps >= 1000:
            atleast_1000 += 1
        
        for dx, dy in [(0, -1), (0, +1), (-1, 0), (+1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < nrows and 0 <= ny < ncols
                and grid[nx][ny] != '#' and (nx, ny) not in seen):
                nsteps = steps + 1 if grid[nx][ny] == '.' else steps
                q.append((nx, ny, nsteps))
                seen.add((nx, ny))
    
    return steps, atleast_1000


if __name__ == '__main__':
    data = '^WNE$'
    data = '^ENWWW(NEEE|SSE(EE|N))$'
    data = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'
    data = get_data(year=2018, day=20)
    regex = data.strip()
    path = trace_path(regex)
    grid = create_grid(path)

    start_x, start_y = 0, 0
    for x, row in enumerate(grid):
        try:
            y = row.index('X')
            if y >= 0:
                start_x, start_y = x, y
                break
        except:
            pass

    steps, atleast_1000 = enumerate_rooms(grid, start_x, start_y)
    print(steps, atleast_1000)
