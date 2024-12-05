from aocd import get_data


def is_valid(grid, r, c):
    if r < 0 or r >= len(grid):
        return False
    if c < 0 or c >= len(grid[0]):
        return False
    return True


def dfs(grid, r, c, s, i, dr, dc):
    if i == len(s):
        return True
    if not is_valid(grid, r, c):
        return False
    if grid[r][c] != s[i]:
        return False
    return dfs(grid, r + dr, c + dc, s, i + 1, dr, dc)


def neighbours():
    return [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def mas_neighbours():
    return [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def find_str(grid, r, c, s):
    return sum(map(lambda d: 1
                   if dfs(grid, r, c, s, 0, d[0], d[1])
                   else 0, neighbours()))


# returns all starts of MAS
def find_mas(grid, r, c, s):
    return set(map(lambda d: (r, c, d)
               if dfs(grid, r, c, s, 0, d[0], d[1])
               else (None, None, None), mas_neighbours()))


def is_x_mas1(mr, mc, d1, all_mas):
    # M  S      S   M
    #  A   or     A
    # M  S      S   M
    comb1 = (mr+2, mc, (-1, 1))
    if comb1 in all_mas:
        # d1 should have right orientation
        return d1 == (1, 1), comb1
    return False, None


def is_x_mas2(mr, mc, d1, all_mas):
    comb2 = (mr+2, mc, (-1, -1))
    if comb2 in all_mas:
        return d1 == (1, -1), comb2
    return False, None


def is_x_mas3(mr, mc, d1, all_mas):
    # M  M      S   S
    #  A   or     A
    # S  S      M   M
    comb1 = (mr, mc+2, (1, -1))
    if comb1 in all_mas:
        # d1 should have right orientation
        return d1 == (1, 1), comb1
    return False, None


def is_x_mas4(mr, mc, d1, all_mas):
    comb2 = (mr, mc+2, (-1, -1))
    if comb2 in all_mas:
        return d1 == (-1, 1), comb2
    return False, None


if __name__ == '__main__':
    data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
    data = get_data(year=2024, day=4)
    grid = data.split('\n')

    nxmas = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            nmatch = find_str(grid, r, c, 'XMAS')
            nxmas += nmatch
    print(nxmas)

    all_mas = set()
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            masloc = find_mas(grid, r, c, 'MAS')
            all_mas |= masloc

    # for all MAS positions, check if an X can be formed.
    n = 0
    for mas in all_mas:
        (mr, mc, d1) = mas
        if mr is None:
            continue
        for fn in (is_x_mas1, is_x_mas2, is_x_mas3, is_x_mas4):
            match, comb = fn(mr, mc, d1, all_mas)
            n += 1 if match else 0

    # print(all_mas)
    # print(all_x_mas, len(all_x_mas))
    print(n)
