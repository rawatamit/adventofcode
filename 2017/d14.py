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


def knot_hash(lengths):
    nums = list(range(256))

    n_round_knot_hash(64, nums, lengths)
    
    xors = []
    for i in range(16):
        block = nums[16*i:16*i+16]
        block_xor = reduce(xor, block)
        assert len(block) == 16
        xors.append(block_xor)
    
    return hex_of_list(xors)


def hextobin(h):
    return bin(int(h, 16))[2:].zfill(len(h) * 4)


def hash_grid(key, dims):
    G = []

    for i in range(dims):
        lengths = [ord(x) for x in f'{key}-{i}']
        lengths.extend([17,31,73,47,23])
        khash = knot_hash(lengths)
        G.append(hextobin(khash))
    
    return G


def part1(key):
    count = 0
    G = hash_grid(key, 128)

    for row in G:
        count += sum(1 for x in hextobin(row) if x == '1')
    
    return count


def neighbors(i, j, G):
    rows = len(G)
    cols = len(G[0])

    di = [1, -1, 0, 0]
    dj = [0, 0, 1, -1]

    for k, _ in enumerate(di):
        ni = di[k] + i
        nj = dj[k] + j

        if 0 <= ni < rows and 0 <= nj < cols:
            yield ni, nj


def explore(G, i, j, cc, seen):
    if (i, j) in seen: return

    seen[(i,j)] = cc
    for ni, nj in neighbors(i, j, G):
        if G[i][j] == '1':
            explore(G, ni, nj, cc, seen)


def part2(key):
    cc = 0
    seen = {}
    G = hash_grid(key, 128)
    rows = len(G)
    cols = len(G[0])

    for i in range(rows):
        for j in range(cols):
            if G[i][j] == '1' and (i, j) not in seen:
                explore(G, i, j, cc, seen)
                cc += 1
     
    return cc


def main():
    # part 1
    # x = part1('amgozmfv')
    # print(x)

    # part 2
    x = part2('amgozmfv')
    print(x)


main()
