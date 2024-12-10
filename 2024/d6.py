from aocd import get_data
import collections


def draw_grid(grid):
    for row in grid:
        print(''.join(row))


def get_rc(pos):
    return int(pos.real), int(pos.imag)


def is_valid(pos, grid):
    x, y = get_rc(pos)
    if x >= 0 and x < len(grid) and y >= 0 and y < len(grid[0]):
        return True
    return False


def getcell(pos, grid):
    x, y = get_rc(pos)
    return grid[x][y]


## do we get into a loop with this grid?
def walk_grid(grid, pos, check_loop=False):
    # starts facing upwards
    dir = (-1+0j)
    # save all directions for a given positions.
    # don't miss a direction that we already traversed because
    # it was not the last direction for that position
    allpos = collections.defaultdict(list)
    allpos[pos].append(dir)
    while True:
        nextpos = pos + dir
        if not is_valid(nextpos, grid):
            break
        if getcell(nextpos, grid) == '#':
            # multiply by -1j to rotate 90 deg right
            # don't update position
            dir = dir * -1j
        else:
            pos = nextpos

        if check_loop:
            # have we already explored this position with this direction
            olddirs = allpos.get(pos, [])
            # there is a loop
            if dir in olddirs:
                return True, allpos
        allpos[pos].append(dir)
    return False, allpos


def part1(grid, pos):
    _, allpos = walk_grid(grid, pos)
    return allpos


def part2(grid, pos):
    # get all cells guard visited. These are the only positions where
    # we want to put a roadblock.
    allpos = part1(grid, pos)
    n = 0
    for cell in allpos:
        # can't block starting position
        if cell == pos:
            continue
        # this should always be an open position '.'
        x, y = get_rc(cell)
        grid[x][y] = '#'
        isloop, _ = walk_grid(grid, pos, check_loop=True)
        n += 1 if isloop else 0
        grid[x][y] = '.'
    return n


if __name__ == '__main__':
    data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
    data = get_data(year=2024, day=6)
    grid = [list(row) for row in data.split('\n')]

    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == '^':
                row[j] = '.'
                pos = (i+j*1j)

    allpos = part1(grid, pos)
    print('part1', len(allpos))

    n = part2(grid, pos)
    print('part2', n)

