from aocd.models import Puzzle


def compress_ranges(ranges):
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    curb, cure = sorted_ranges[0]
    l = []

    for i in range(1, len(sorted_ranges)):
        r = sorted_ranges[i]

        if r[0] > cure + 1:
            # new range
            l.append((curb, cure))
            curb, cure = r
        else:
            cure = max(cure, r[1])
    
    l.append((curb, cure))
    return l


if __name__ == '__main__':
    puzzle = Puzzle(year=2016, day=20)
    data = puzzle.input_data

    ranges = [[int(x) for x in r.split('-')]
                for r in data.split('\n')]
    
    assert compress_ranges([(1, 4), (5, 7), (6, 8), (9, 12), (10, 11), (14, 15)]) == [(1, 12), (14, 15)]

    cranges = compress_ranges(ranges)

    # part 1
    print(cranges[0][1]+1)

    # part 2
    # This works because the last range includes the maximum IP.
    # If this was not the case, then subtracting banned ips from 2**32
    # would be the only correct solution.
    print(sum([cranges[i][0] - cranges[i-1][1]-1 for i in range(1, len(cranges))]))
