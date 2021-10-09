from itertools import cycle
import math


def num_digits(x):
    assert x > 0
    return math.ceil(math.log(x, 10)) if x > 1 else 1


def cycle_for(x, n):
    for _ in range(n):
        yield x


def cycle_patterns(pos):
    base_pattern = [0, 1, 0, -1]
    first_element = True

    for x in cycle(base_pattern):
        for y in cycle_for(x, pos):
            if first_element:
                first_element = False
                continue
            yield y


def compute_position(x, pos):
    i = 0
    val = 0
    for y in cycle_patterns(pos):
        if i < len(x):
            val += x[i] * y
            i += 1
        else:
            break
    return abs(val) % 10


def compute_phase(x):
    ret = x[:]

    for i in range(1, len(x)+1):
        ret[i-1] = compute_position(x, i)
    
    return ret

def compute_nphase(x, nphase):
    pos = num_digits(x)
    l = [0 for _ in range(pos)]
    i = pos - 1
    while x > 0:
        l[i] = x % 10
        i -= 1
        x //= 10

    for i in range(nphase):
        l = compute_phase(l)
    
    return ''.join(map(str, l))


def part2_one_iteration(bignum, offset):
    last_index = len(bignum) - 1
    cur_index = last_index

    while cur_index >= offset:
        if cur_index < last_index:
            val = bignum[cur_index] + bignum[cur_index + 1]
            bignum[cur_index] = val % 10
        cur_index -= 1

def part2_n_iteration(bignum, offset, n):
    for _ in range(n):
        part2_one_iteration(bignum, offset)

def main():
    with open('d16.txt') as fin:
        # x = int(fin.read())
        num = [int(x) for x in fin.read().strip()]
    
    # part 1
    # y = compute_nphase(x, 100)
    # print(y)

    # part 2
    bignum = list(range(len(num) * 10000))
    it = cycle(num)
    for i in range(len(bignum)):
        bignum[i] = next(it)
    
    offset = int(''.join(map(str, num[:7])))
    part2_n_iteration(bignum, offset, 100)
    print(bignum[offset:offset+8])

main()
