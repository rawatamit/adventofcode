from aocd.models import Puzzle
import re


def change_rect(a, b, c, d, grid, fn=lambda x: x):
    for i in range(a, c+1):
        for j in range(b, d+1):
            grid[i][j] = fn(grid[i][j])


if __name__ == '__main__':
    puzzle = Puzzle(year=2015, day=6)
    data = puzzle.input_data

    # part 1
    grid = [[0 for _ in range(1000)]
            for _ in range(1000)]

    for line in data.split('\n'):
        a, b, c, d = [int(x) for x in re.findall(r'\d+', line)]

        if line.startswith('turn on'):
            change_rect(a, b, c, d, grid, fn=lambda _: 1)
        elif line.startswith('turn off'):
            change_rect(a, b, c, d, grid, fn=lambda _: 0)
        elif line.startswith('toggle'):
            change_rect(a, b, c, d, grid,
                        fn=lambda x: 1 if x == 0 else 0)
    
    count = sum(grid[i][j]
                for i in range(1000)
                for j in range(1000))
    print(count)

    # part 2
    grid = [[0 for _ in range(1000)]
            for _ in range(1000)]

    for line in data.split('\n'):
        a, b, c, d = [int(x) for x in re.findall(r'\d+', line)]

        if line.startswith('turn on'):
            change_rect(a, b, c, d, grid, fn=lambda x: x + 1)
        elif line.startswith('turn off'):
            change_rect(a, b, c, d, grid,
                        fn=lambda x: 0 if x <= 0 else x - 1)
        elif line.startswith('toggle'):
            change_rect(a, b, c, d, grid, fn=lambda x: x + 2)
    
    count = sum(grid[i][j]
        for i in range(1000)
        for j in range(1000))
    print(count)
