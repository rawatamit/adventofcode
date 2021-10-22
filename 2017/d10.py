from functools import reduce
from operator import xor


# both start and stop are inclusive
def reverse(l, start, stop):
    n = len(l)
    to_reverse = (stop - start + 1) // 2
    i = start % n
    j = stop % n

    while to_reverse > 0:
        l[i], l[j] = l[j], l[i]

        i = (i + 1) % n
        j = (j - 1) % n

        to_reverse -= 1


def n_round_knot_hash(n, nums, lengths):
    curpos, skip_size = 0, 0

    for _ in range(n):
        for length in lengths:
            reverse(nums, curpos, curpos + length - 1)
            curpos += length + skip_size
            skip_size += 1

    return curpos, skip_size


def hex_of_int(i):
    return f'{i:02x}'


def hex_of_list(l):
    return ''.join(hex_of_int(x) for x in l)


def part1(lengths):
    nums = list(range(256))
    n_round_knot_hash(1, nums, lengths)
    return nums[0] * nums[1]


def part2(lengths):
    nums = list(range(256))

    n_round_knot_hash(64, nums, lengths)
    
    xors = []
    for i in range(16):
        block = nums[16*i:16*i+16]
        block_xor = reduce(xor, block)
        assert len(block) == 16
        xors.append(block_xor)
    
    return hex_of_list(xors)


def run_test():
    nums = [0, 1, 2, 3, 4]
    reverse(nums, 0, 2)
    assert nums == [2, 1, 0, 3, 4]

    nums = [0, 1, 2, 3, 4]
    reverse(nums, 3, 6)
    assert nums == [4, 3, 2, 1, 0]

    nums = [0, 1, 2, 3, 4]
    reverse(nums, 1, 5)
    assert nums == [1, 0, 4, 3, 2]


def main():
    lengths_p2 = []
    with open('d10.txt') as fin:
        for line in fin:
            if line.strip():
                lengths = [int(x) for x in line.split(',')]
                lengths_p2 = [ord(x) for x in line.strip()]
    
    run_test()

    # part 1
    x = part1(lengths)
    print(x)

    # part 2
    lengths_p2.extend([17,31,73,47,23])
    x = part2(lengths_p2)
    print(x)


main()
