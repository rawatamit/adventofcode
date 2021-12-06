def power_level(coords, serial_no):
    x, y = coords
    rack_id = x + 10
    power_level = (rack_id * y + serial_no) * rack_id
    return (power_level % 1000) // 100 - 5


def getcell(grid, x, y):
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        return grid[x][y]
    return 0


def make_summed_grid(rows, cols, serial_no):
    rbegin, rend = rows
    cbegin, cend = cols
    grid = [[0 for _ in range(cend+1)] for _ in range(rend+1)]

    for x in range(rbegin, rend+1):
        for y in range(cbegin, cend+1):
            grid[x][y] = power_level((x, y), serial_no) + getcell(grid, x, y-1) + getcell(grid, x-1, y) - getcell(grid, x-1, y-1)
    
    return grid


def grid_rect(top_left, bottom_right, grid):
    trow, tcol = top_left
    brow, bcol = bottom_right
 
    return [[grid[i][j]
               for j in range(tcol, bcol+1)]
               for i in range(trow, brow+1)]


def summed_area_table(grid):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            grid[x][y] = grid[x][y] + getcell(grid, x, y-1) + getcell(grid, x-1, y) - getcell(grid, x-1, y-1)


def power_fuel_cell_summed(top_left, bottom_right, grid):
    trow, tcol = top_left
    brow, bcol = bottom_right
    return grid[brow][bcol] + grid[trow][tcol] - grid[brow][tcol] - grid[trow][bcol]


def power_fuel_cell(top_left, bottom_right, serial_no):
    trow, tcol = top_left
    brow, bcol = bottom_right

    return sum(power_level((i, j), serial_no)
               for i in range(trow, brow+1)
               for j in range(tcol, bcol+1))


def fuel_cells(rows, cols, size):
    rbegin, rend = rows
    cbegin, cend = cols

    for i in range(rbegin, rend):
        for j in range(cbegin, cend):
            top_left = (i, j)
            bottom_right = (i+size-1, j+size-1)
            if bottom_right[0] <= rend and bottom_right[1] <= cend:
                yield top_left, bottom_right


def max_fuel_cell(rows, cols, size_range, serial_no):
    max_power = -1
    max_top_left = None
    max_size = -1
    power_grid = make_summed_grid(rows, cols, serial_no)

    for size in size_range:
        for top_left, bottom_right in fuel_cells(rows, cols, size):
            #cell_power = power_fuel_cell(top_left, bottom_right, serial_no)

            ## Summation does not include top_left coordinates
            ## to get the right sum, use top_left - (-1, -1)
            ntop_left = top_left[0] - 1, top_left[1] - 1
            cell_power = power_fuel_cell_summed(ntop_left, bottom_right, power_grid)

            if cell_power > max_power:
                max_power = cell_power
                max_top_left = top_left
                max_size = size
    
    return max_power, max_size, max_top_left


if __name__ == '__main__':
    assert power_level((3,5), 8) == 4
    assert power_level((122,79), 57) == -5
    assert power_level((217,196), 39) == 0
    assert power_level((101,153), 71) == 4

    assert max_fuel_cell((1, 300), (1, 300), [3], 18) == (29, 3, (33, 45))
    assert max_fuel_cell((1, 300), (1, 300), [3], 42) == (30, 3, (21, 61))
    print(max_fuel_cell((1, 300), (1, 300), [3], 6548))
    print(max_fuel_cell((1, 300), (1, 300), range(1, 301), 6548))

    # Example from https://en.wikipedia.org/wiki/Summed-area_table
    # grid = [[31, 2, 4, 33, 5, 36],
    #         [12,  26, 9, 10, 29, 25],
    #         [13, 17, 21, 22, 20, 18],
    #         [24, 23, 15, 16, 14, 19],
    #         [30, 8, 28, 27, 11, 7],
    #         [1, 35, 34, 3, 32, 6]]
    
    #print(grid)
    #print(grid_rect((3,2), (4,4), grid))
    #summed_area_table(grid)
    #print(grid)
    #print(grid_rect((3,2), (4,4), grid))
    #print(power_fuel_cell_summed((3-1,2-1), (4,4), grid))
