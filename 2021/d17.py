from aocd.models import Puzzle
import re


def trajectory(xrange, yrange, vel_x, vel_y):
    x, y = 0, 0
    max_y = -float('inf')

    for _ in range(1000):
        max_y = max(max_y, y)
        if x in xrange and y in yrange:
            return True, max_y
        x += vel_x
        y += vel_y
        vel_x += -1 if vel_x > 0 else (1 if vel_x < 0 else 0)
        vel_y -= 1
    
    return False, -1


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=17)
    data = puzzle.input_data

    data = 'target area: x=20..30, y=-10..-5'
    x_min, x_max, y_min, y_max = [int(x) for x in re.findall(r'-?\d+', data)]
    xrange = set(range(x_min, x_max+1))
    yrange = set(range(y_min, y_max+1))

    all_max_y = -float('inf')
    max_vel_x, max_vel_y = 0, 0
    vels = set()
    #res, max_y = trajectory(xrange, yrange, 6, 9)
    #exit(0)

    for vel_x in range(x_max+10):
        for vel_y in range(y_min-1, -y_max+150):
            res, max_y = trajectory(xrange, yrange, vel_x, vel_y)
            if res:
                vels.add((vel_x, vel_y))
                all_max_y = max(all_max_y, max_y)

    print(all_max_y)
    print(len(vels))
