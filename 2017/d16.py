import string


def spin(s, inst):
    for _ in range(int(inst[1:])):
        v = s.pop()
        s.insert(0, v)


def exchange(s, inst):
    a, b = [int(x) for x in inst[1:].split('/')]
    s[a], s[b] = s[b], s[a]


def partner(s, inst):
    a, b = inst[1:].split('/')
    ai = s.index(a)
    bi = s.index(b)
    s[ai], s[bi] = s[bi], s[ai]


def run_tests():
    s = [x for x in 'abcde']

    spin(s, 's1')
    exchange(s, 'x3/4')
    partner(s, 'pe/b')

    assert s == ['b', 'a', 'e', 'd', 'c']


def dance(s, insts):
    for inst in insts:
        if inst[0] == 's':
            spin(s, inst)
        elif inst[0] == 'x':
            exchange(s, inst)
        elif inst[0] == 'p':
            partner(s, inst)


def find_repeat(s, insts, niter=1):
    hash = {}
    i = 0

    while True:
        r = ''.join(s)

        if r in hash:
            cycle_start = hash[r]
            p = (1000000000 % (i - cycle_start)) - cycle_start
            for k,v in hash.items():
                if v == p:
                    print(k)
            break

        dance(s, insts)
        hash[r] = i
        i += 1


def main():
    run_tests()

    s = [x for x in string.ascii_lowercase[:16]]

    with open('d16.txt') as fin:
        insts = fin.read().strip().split(',')
    
    # part 1
    # dance(s, insts)
    # print(''.join(s))

    # part 2
    find_repeat(s, insts, 40)


main()
