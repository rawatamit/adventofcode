from aocd.models import Puzzle


def move_sea_cucumber(l, orientation):
    i = 0
    nl = ['' for _ in range(len(l))]
    is_modified = False

    while i < len(l):
        ni = 0 if i == len(l) - 1 else i + 1
        if l[i] == orientation and l[ni] == '.':
            nl[i] = '.'
            nl[ni] = orientation
            i += 2
            is_modified = True
        else:
            nl[i] = l[i]
            i += 1
    return is_modified, nl


def move_east_row(row):
    return move_sea_cucumber(row, '>')


def move_vertical_col(col):
    return move_sea_cucumber(col, 'v')


def move_one_step(G):
    is_modified = False
    nG = []

    for row in G:
        modified, row = move_east_row(row)
        is_modified = is_modified or modified
        nG.append(row)

    col_idx = 0
    for col in zip(*nG):
        modified, ncol = move_vertical_col(col)
        is_modified = is_modified or modified
        for r in range(len(nG)):
            nG[r][col_idx] = ncol[r]
        col_idx += 1

    return is_modified, nG


def move_until_stop(G):
    steps = 0

    while True:
        is_modified, G = move_one_step(G)
        steps += 1
        if not is_modified: return steps
    
    return -1


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=25)

    data = '''v...>>.vv>
            .vv>>.vv..
            >>.>v>...v
            >>v>>.>.v.
            v>v.vv.v..
            >.>>..v...
            .vv..>.>v.
            v.v..>>v.v
            ....v..v.>'''

    data = puzzle.input_data

    G = []
    for line in data.split('\n'):
        line = line.strip()
        G.append([c for c in line])
    
    print(move_until_stop(G))
