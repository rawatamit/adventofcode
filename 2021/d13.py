from aocd.models import Puzzle


def grid_corners(coords):
    min_x = min(x for x,_ in coords)
    max_x = max(x for x,_ in coords)
    min_y = min(y for _,y in coords)
    max_y = max(y for _,y in coords)
    return (min_x, min_y), (max_x, max_y)


def draw_grid(coords):
    (min_x, min_y), (max_x, max_y) = grid_corners(coords)

    grid = [[' ' for _ in range(max_x + 1)]
            for _ in range(max_y + 1)]
    
    for x, y in coords:
        grid[y][x] = '#'
    
    for row in grid:
        print(''.join(row))


def fold_y(x, y, y_axis):
    return (x, -abs(y - y_axis) + y_axis)


def transform_along_y(coords, y_axis):
    return list(map(lambda xy: fold_y(xy[0], xy[1], y_axis), coords))


def fold_x(x, y, x_axis):
    return (-abs(x - x_axis) + x_axis, y)


def transform_along_x(coords, x_axis):
    return list(map(lambda xy: fold_x(xy[0], xy[1], x_axis), coords))


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=13)

    data = '''
    6,10
    0,14
    9,10
    0,3
    10,4
    4,11
    6,0
    6,12
    4,1
    0,13
    10,12
    3,4
    3,0
    8,4
    1,10
    2,14
    8,10
    9,0

    fold along y=7
    fold along x=5'''

    coords = []
    data = puzzle.input_data

    for line in data.split('\n'):
        line = line.strip()

        if line and line.startswith('fold'):
            axis, value = line.split('=')
            axis = axis[-1]
            value = int(value)

            if axis[-1] == 'y':
                coords = transform_along_y(coords, value)
                #draw_grid(coords)
            elif axis[-1] == 'x':
                coords = transform_along_x(coords, value)
                #draw_grid(coords)
            #break
        elif line:
            x, y = [int(k) for k in line.split(',')]
            coords.append((x, y))

    # part 1, use in conjunction with break above
    print(len(set(coords)))

    # part 2, make all folds
    draw_grid(coords)
