from aocd import get_data


def parse_sections(s):
    elf1, elf2 = s.split(',')
    elf1_s, elf1_e = [int(x) for x in elf1.split('-')]
    elf2_s, elf2_e = [int(x) for x in elf2.split('-')]
    return (elf1_s, elf1_e), (elf2_s, elf2_e)


def is_contained(a, b):
    # is b fully contained in a?
    return b[0] >= a[0] and b[1] <= a[1]


def is_overlap(a, b):
    # do a and b overlap?
    return b[0] >= a[0] and a[1] >= b[0]


if __name__ == '__main__':
    data = '''2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8'''
    data = get_data(year=2022, day=4)

    # part 1
    full_contained = 0
    for line in data.splitlines():
        elf1, elf2 = parse_sections(line)
        if is_contained(elf1, elf2) or is_contained(elf2, elf1):
            full_contained += 1
    print(full_contained)

    # part 2
    overlap = 0
    for line in data.splitlines():
        elf1, elf2 = parse_sections(line)
        if is_overlap(elf1, elf2) or is_overlap(elf2, elf1):
            overlap += 1
    print(overlap)
