from aocd import get_data
import json
import itertools


def in_order(x, y, indent=0):
    #print(f'{" "*indent}Compare {x} vs {y}')
    # both are ints
    if isinstance(x, int) and isinstance(y, int):
        if x < y:
            return True
        if x > y:
            return False

    # both are lists
    elif isinstance(x, list) and isinstance(y, list):
        if not x and y:
            return True
        if not y and x:
            return False

        for xs, ys in itertools.zip_longest(x, y, fillvalue=[]):
            #print(xs, ys)
            # None means equal
            res = in_order(xs, ys, indent+2)
            if res is not None:
                return res
        return in_order(len(x), len(y))

    elif isinstance(x, int):
        #print(f'{" "*indent}Mixed type {x}, retry')
        return in_order([x], y, indent+2)
    elif isinstance(y, int):
        #print(f'{" "*indent}Mixed type {y}, retry')
        return in_order(x, [y], indent+2)


def sort_packets(all_packets):
    # probably wrong sorting
    for i in range(len(all_packets)):
        x = all_packets[i]
        # place i in the correct position
        for j in range(i):
            if not in_order(all_packets[j], x):
                all_packets[j], all_packets[i] = all_packets[i], all_packets[j]


if __name__ == '__main__':
    data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
    data = get_data(year=2022, day=13)

    total = 0
    index = 1
    pair = []
    all_packets = []
    for line in data.split('\n'):
        if len(pair) < 2:
            pair.append(json.loads(line))
            all_packets.append(pair[-1])
        else:
            res = in_order(pair[0], pair[1])
            # in order
            if res:
                total += index
            assert res is not None
            pair = []
            index += 1

    # last pair
    res = in_order(pair[0], pair[1])
    assert res is not None
    if res:
        total += index

    print('part1', total)

    # add divider packets
    div_pkt1 = [[2]]
    all_packets.append(div_pkt1)
    div_pkt2 = [[6]]
    all_packets.append(div_pkt2)
    sort_packets(all_packets)
    print('part2', (all_packets.index(div_pkt1)+1) * (all_packets.index(div_pkt2)+1))

