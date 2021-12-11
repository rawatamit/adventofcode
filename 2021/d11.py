from logging import BufferingFormatter
from aocd.models import Puzzle
from bs4 import builder


def make_grid(data):
    grid = [[int(x) for x in row]
            for row in data]
    return grid


def draw_grid(grid):
    for i in range(len(grid)):
        display_row = [str(grid[i][j])
                        for j in range(len(grid[i]))]
        print(''.join(display_row))
 

def neigbors(i, j, grid):
    di = [1, -1, 0, 0, -1, -1, 1, 1]
    dj = [0, 0, 1, -1, 1, -1, -1, 1]

    for k,_ in enumerate(di):
        ni = i + di[k]
        nj = j + dj[k]

        if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
            yield ni, nj


def resolve_flash_points(buffer, flash_points):
    # Q is a set because we will keep entries that are being processed in it.
    # When iterating over neigbors, if we add a duplicate entry that is already
    # being processed, it is only added once.
    
    Q = set(flash_points)
    completed = set()
    flashes = 0

    while Q:
        i, j = Q.pop()
        flashes += 1

        for ni, nj in neigbors(i, j, buffer):
            if (ni, nj) not in completed:
                buffer[ni][nj] += 1
                if buffer[ni][nj] > 9:
                    Q.add((ni, nj))
        
        completed.add((i, j))
        buffer[i][j] = 0

    return flashes


def simulate_one_step(grid, buffer):
    flash_points = []

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # energy level increase by 1
            buffer[i][j] = 1 + grid[i][j]

            if buffer[i][j] > 9:
                flash_points.append((i, j))
    
    return resolve_flash_points(buffer, flash_points)


def simulation(grid, steps=1):
    buffer = [[0 for _ in range(len(grid[i]))]
              for i in range(len(grid))]
    
    total_flashes = 0

    for _ in range(steps):
        total_flashes += simulate_one_step(grid, buffer)
        grid, buffer = buffer, grid
    
    return total_flashes


def simulate_till_all(grid):
    buffer = [[0 for _ in range(len(grid[i]))]
              for i in range(len(grid))]
    
    n = len(grid) * len(grid[0])
    step = 0
    
    while True:
        flashes = simulate_one_step(grid, buffer)
        step += 1

        if flashes == n:
            return step
        
        grid, buffer = buffer, grid


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=11)
    data = puzzle.input_data

    grid = make_grid(['11111',
                      '19991',
                      '19191',
                      '19991',
                      '11111'])
    
    grid = make_grid(['5483143223',
                      '2745854711',
                      '5264556173',
                      '6141336146',
                      '6357385478',
                      '4167524645',
                      '2176841721',
                      '6882881134',
                      '4846848554',
                      '5283751526'])
    
    grid = make_grid(data.split('\n'))

    # NOTE: run part 1 and part 2 independently as grid is modified in both.
    # Or pass a new copy to both to avoid this.
    # Or add 100 to the answer printed for part 2 below, as we simulate from
    # 100 steps onward.

    # part 1
    print(simulation(grid, steps=100))

    # part 2
    print(100 + simulate_till_all(grid))
