from aocd.models import Puzzle


def neigbors(i, j, grid):
    di = [1, -1, 0, 0]
    dj = [0, 0, 1, -1]

    for k,_ in enumerate(di):
        ni = i + di[k]
        nj = j + dj[k]

        if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
            yield ni, nj


def is_low_point(i, j, grid):
    nvalues = [int(grid[ni][nj])
                for ni, nj in neigbors(i, j, grid)]
    
    cell_value = int(grid[i][j])
    nvalues.append(cell_value)
    min_val = min(nvalues)
    return min(nvalues) == cell_value and len([x for x in nvalues if x == min_val]) == 1


def can_be_basin_point(i, j, grid):
    return int(grid[i][j]) != 9


def is_downward_flow(i, j, ni, nj, grid):
    return int(grid[i][j]) < int(grid[ni][nj])


def search_grid_brute(grid):
    count = 0
    total_risk_level = 0

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if is_low_point(i, j, grid):
                count += 1
                total_risk_level += 1 + int(grid[i][j])
    
    return count, total_risk_level


def mark_cc(i, j, grid, seen_grid):
    if seen_grid[i][j]: return 0
    seen_grid[i][j] = True

    for ni, nj in neigbors(i, j, grid):
        if can_be_basin_point(ni, nj, grid) and is_downward_flow(i, j, ni, nj, grid):
            mark_cc(ni, nj, grid, seen_grid)


def dfs(i, j, grid, seen):
    if (i, j) in seen: return 0
    seen.add((i, j))

    cc_size = 1
    for ni, nj in neigbors(i, j, grid):
        if grid[ni][nj] and (ni, nj) not in seen:
            cc_size += dfs(ni, nj, grid, seen)
    return cc_size


def find_cc(grid):
    seen_grid = [[False for _ in range(len(grid[i]))]
                 for i in range(len(grid))]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if can_be_basin_point(i, j, grid):
                mark_cc(i, j, grid, seen_grid)

    #new_grid = []
    #for row in seen_grid:
    #    display_row = [('.' if x else '#') for x in row]
    #    print(''.join(display_row))
    #    new_grid.append(display_row)

    seen = set()
    basins = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if seen_grid[i][j] and not (i, j) in seen:
                cc_size = dfs(i, j, seen_grid, seen)
                basins.append(cc_size)
    
    mul_basin = 1
    for x in sorted(basins)[-3:]:
        mul_basin *= x
    return mul_basin


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=9)
    data = puzzle.input_data

    grid = ['2199943210',
            '3987894921',
            '9856789892',
            '8767896789',
            '9899965678']

    grid = data.split('\n')
    print(find_cc(grid))
