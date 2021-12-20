from aocd.models import Puzzle
from itertools import groupby


def look_and_say(s, times=1):
    cur_s = [int(c) for c in s]

    for _ in range(times):
        new_s = []
        for k, v in groupby(cur_s):
            new_s.extend([len(list(v)), k])
        cur_s = new_s
    
    return cur_s


if __name__ == '__main__':
    puzzle = Puzzle(year=2015, day=10)

    data = '1'
    data = puzzle.input_data

    s = look_and_say(data, 40)
    print(len(s))

    s = look_and_say(data, 50)
    print(len(s))