from aocd.models import Puzzle

SAFE = 0
TRAP = 1


def get_tile(i, row):
    tile_map = {'^': TRAP, '.': SAFE}
    return (SAFE if i < 0 or i >= len(row)
        else tile_map[row[i]])


def is_trap(i, row):
    left = get_tile(i - 1, row)
    center = get_tile(i, row)
    right = get_tile(i + 1, row)

    if (left, center, right) == (TRAP, TRAP, SAFE):
        return True
    if (left, center, right) == (SAFE, TRAP, TRAP):
        return True
    if (left, center, right) == (TRAP, SAFE, SAFE):
        return True
    if (left, center, right) == (SAFE, SAFE, TRAP):
        return True
    
    return False


def get_next_row(row):
    l = [('^' if is_trap(i, row) else '.')
            for i in range(len(row))]
    return ''.join(l)


def generate_rows(first_row, n=1):
    currow = first_row

    for _ in range(n):
        # first row is also yielded
        yield currow
        currow = get_next_row(currow)


if __name__ == '__main__':
    puzzle = Puzzle(year=2016, day=18)
    first_row = puzzle.input_data

    #first_row = '.^^.^.^^^^'

    total_safe_tiles = 0
    for row in generate_rows(first_row, 400000):
        safe_tiles = len([x for x in row if x == '.'])
        total_safe_tiles += safe_tiles
    
    print(total_safe_tiles)
