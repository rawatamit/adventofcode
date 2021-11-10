def numpad1():
    return [['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9']]


def numpad2():
    return [['', '', '1', '', ''],
            ['', '2', '3', '4', ''],
            ['5', '6', '7', '8', '9'],
            ['', 'A', 'B', 'C', ''],
            ['', '', 'D', '', '']]


def is_valid(grid, x, y):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid) and grid[y][x] != ''


def update_position(grid, curpos, cmd):
    cmd_map = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

    dx, dy = cmd_map[cmd]
    x, y = (curpos[0] + dx, curpos[1] + dy)
    return (x, y) if is_valid(grid, x, y) else curpos


def part12(init_pos, grid):
    curpos = init_pos
    keycode = []

    with open('d2.txt') as fin:
        for line in fin:
            for cmd in line.strip():
                curpos = update_position(grid, curpos, cmd)
            x, y = curpos
            keycode.append(grid[y][x])
    
    print(''.join(keycode))


if __name__ == '__main__':
    # part 1, button 5 is at (1, 1)
    part12((1, 1), numpad1())

    # part 2, button 5 is at (2, 0)
    part12((2, 0), numpad2())
