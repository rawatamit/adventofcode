from aocd import get_data
from collections import Counter


def is_lock(lines):
    if '.' in lines[0]:
        return False
    if '#' in lines[-1]:
        return False
    return True


def find_height(lines, ch):
    ht = []
    for i in range(len(lines[0])):
        for j in range(len(lines)):
            if lines[j][i] == ch:
                ht.append(j)
                break
    return ht


def lock_height(lines):
    ht = find_height(lines, '.')
    return ht


def key_height(lines):
    ht = find_height(lines, '#')
    return [len(lines) - x for x in ht]


if __name__ == '__main__':
    data = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
    data = get_data(year=2024, day=25)
    lines = []
    locks = []
    keys = []
    for line in data.split('\n'):
        if line:
            lines.append(line)
        else:
            if is_lock(lines):
                locks.append(lock_height(lines))
            else:
                keys.append(key_height(lines))
            lines = []

    # last entry
    if is_lock(lines):
        locks.append(lock_height(lines))
    else:
        keys.append(key_height(lines))

    total = 0
    for lock in locks:
        for key in keys:
            ht = [7 - lock[i] - key[i]
                    for i in range(len(key))]
            if not any(map(lambda x: x < 0, ht)):
                total += 1

    print('part1', total)

