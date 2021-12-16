from aocd.models import Puzzle
from collections import defaultdict


def add_tuple(a, b):
    return tuple(a_i + b_i for a_i, b_i in zip(a, b))


def update_loc(cur_loc, c):
    if c == '^':
        return add_tuple(cur_loc, (0, 1))
    elif c == '<':
        return add_tuple(cur_loc, (-1, 0))
    elif c == '>':
        return add_tuple(cur_loc, (1, 0))
    else:
        return add_tuple(cur_loc, (0, -1))


def gift(start, instructions):
    visited = defaultdict(int)
    visited[start] = 1
    cur_loc = start

    for c in instructions:
        cur_loc = update_loc(cur_loc, c)
        visited[cur_loc] += 1
    
    return visited


if __name__ == '__main__':
    puzzle = Puzzle(year=2015, day=3)
    data = puzzle.input_data

    start = (0, 0)
    print(len(gift(start, data)))

    start = (0, 0)
    santa_insts = [data[i] for i in range(0, len(data), 2)]
    robo_insts = [data[i] for i in range(1, len(data), 2)]

    santa_visited = set(gift(start, santa_insts).keys())
    robo_visited = set(gift(start, robo_insts).keys())

    print(len(santa_visited | robo_visited))
