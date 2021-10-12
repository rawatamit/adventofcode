import copy


def neigbors(i, j, grid):
    di = [1, -1, 0, 0]
    dj = [0, 0, 1, -1]

    for k,_ in enumerate(di):
        ni = i + di[k]
        nj = j + dj[k]

        if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
            yield ni, nj


def neigbor_bugs(i, j, grid):
    bug_count = 0
    for ni, nj in neigbors(i, j, grid):
        if grid[ni][nj] == '#':
            bug_count += 1
    return bug_count


def one_step(cur_grid, next_grid):
    for i in range(len(cur_grid)):
        for j in range(len(cur_grid[0])):
            bug_count = neigbor_bugs(i, j, cur_grid)

            cell = cur_grid[i][j]
            next_grid[i][j] = cell

            if cell == '#':
                if bug_count != 1:
                    next_grid[i][j] = '.'
            elif bug_count in (1, 2):
                next_grid[i][j] = '#'


def draw(grid):
    for row in grid:
        print(''.join(row))


def forever_step(grid):
    next_grid = copy.deepcopy(grid)

    while True:
        yield grid
        one_step(grid, next_grid)
        save = grid
        grid = next_grid
        next_grid = save


def biodiversity_rating(grid):
    rating = 0
    cell_rating = 1

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '#':
                rating += cell_rating
            cell_rating *= 2
    
    return rating


def part1(grid):
    seen = set()

    for ngrid in forever_step(grid):
        x = biodiversity_rating(ngrid)
        if x in seen:
            return x
        else:
            seen.add(x)


def main():
    grid = []
    with open('d24.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                grid.append([x for x in line])
    
    x = part1(grid)
    print(x)


main()
