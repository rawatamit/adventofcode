from aocd import get_data


def is_valid_cell(x, y, grid):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def num_from_loc(locs):
    # locs is a list of pairs with (x, y) cell for each digit
    # sort locs by y digit, x should always be the same for each
    locs.sort(key=lambda x: x[1])
    return int(''.join([grid[x][y] for x,y in locs]))


def get_nums(grid, part2=False):
    numlocs = set()
    nums = []
    dx = [-1, -1, -1,  0,  0, +1, +1, +1]
    dy = [-1,  0, +1, -1, +1, -1,  0, +1]
    gear_ratios = []

    for x, row in enumerate(grid):
        for y, col in enumerate(row):
            # skip . and symbols
            if col == '.' or col.isdigit():
                continue
            # only concerned with gears in part 2
            if part2 and col != '*':
                continue
            # iterate over all neighbors
            gear_nums = [] # numbers next to a gear
            for i, di in enumerate(dx):
                nx = di + x
                ny = dy[i] + y
                if is_valid_cell(nx, ny, grid) and grid[nx][ny].isdigit() and (nx, ny) not in numlocs:
                    newnum = [(nx, ny)]
                    cury = ny + 1
                    while is_valid_cell(nx, cury, grid) and grid[nx][cury].isdigit():
                        newnum.append((nx, cury))
                        numlocs.add((nx, cury))
                        cury += 1

                    cury = ny - 1
                    while is_valid_cell(nx, cury, grid) and grid[nx][cury].isdigit():
                        newnum.append((nx, cury))
                        numlocs.add((nx, cury))
                        cury -= 1

                    num = num_from_loc(newnum)
                    nums.append(num)
                    # adjacent to a gear
                    gear_nums.append(num)

            if len(gear_nums) == 2:
                gear_ratios.append(gear_nums[0] * gear_nums[1])

    return nums, gear_ratios


if __name__ == '__main__':
    data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    data = get_data(year=2023, day=3)
    grid = [line.strip() for line in data.splitlines()]

    # part 1
    nums, _ = get_nums(grid)
    print('part1', sum(nums))
    
    # part 2
    nums, gear_ratios = get_nums(grid, True)
    print('part2', sum(gear_ratios))

