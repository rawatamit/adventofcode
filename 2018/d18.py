from aocd import get_data

def adjacent(i, j):
    di = [-1, -1, -1,  0, 0,  1, 1, 1]
    dj = [-1,  0,  1, -1, 1, -1, 0, 1]
    return [(i + di[k], j + dj[k]) for k in range(len(di))]


def adjacent_cells(i, j, grid, nrows, ncols):
    trees = 0
    lumberyard = 0
    for ni, nj in adjacent(i, j):
        if 0 <= ni < nrows and 0 <= nj < ncols:
            if grid[ni][nj] == '|':
                trees += 1
            elif grid[ni][nj] == '#':
                lumberyard += 1
    return trees, lumberyard


def next_state(state):
    nrows = len(state)
    ncols = len(state[0])
    next_grid = []
    for i in range(nrows):
        next_row = []
        for j in range(ncols):
            trees, lumberyard = adjacent_cells(i, j, grid, nrows, ncols)
            if grid[i][j] == '.' and trees >= 3:
                next_row.append('|')
            elif grid[i][j] == '|' and lumberyard >= 3:
                next_row.append('#')
            elif grid[i][j] == '#':
                if lumberyard > 0 and trees > 0:
                    next_row.append('#')
                else:
                    next_row.append('.')
            else:
                next_row.append(grid[i][j])
        next_grid.append(''.join(next_row))
    return next_grid


def resource_value(grid):
    trees = 0
    lumberyard = 0
    for row in grid:
        for cell in row:
            if cell == '|':
                trees += 1
            elif cell == '#':
                lumberyard += 1
    return trees * lumberyard


def print_grid(grid):
    for row in grid:
        print(row)


if __name__ == '__main__':
    data = '''.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.'''
    data = get_data(year=2018, day=18)
    grid = [s.strip() for s in data.splitlines()]

    # part 1
    # times = 10
    # for _ in range(times):
    #     grid = next_state(grid)
    #print_grid(grid)
    # print(resource_value(grid))

    # part 2
    times = 1000#000000
    resvals = []
    seen = set()
    countdown = 34
    countdown_activate = False
    saved_resvals = []
    last_resval = 0
    for i in range(times):
        grid = next_state(grid)
        val = resource_value(grid)
        #print(val, last_resval, val - last_resval)
        last_resval = val
        if val in seen and i == 465:
            #print(f'seen {val}, gen {i}')
            countdown_activate = True
        if countdown_activate:
            saved_resvals.append(val)
            if countdown == 0:
                break
            else:
                countdown -= 1
        seen.add(val)
        resvals.append(val)
    
    # after 465 states, grid repeats with a period of 34
    repeats = 1000000000 - 465
    # need to find index of the 34 repeating values where we
    # will be at 1000000000th iteration. because list indices
    # start from 0, we subtract 1 to find correct index.
    print(saved_resvals[repeats % len(saved_resvals) - 1])
