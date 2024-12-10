from aocd import get_data
import re

if __name__ == '__main__':
    data = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    data = get_data(year=2024, day=3)

    matches = re.findall('mul\((\d+),(\d+)\)', data)
    print('part1', sum(int(a) * int(b) for a, b in matches))

    #data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    matches = re.findall('do\(\)|don\'t\(\)|mul\(\d+,\d+\)', data)

    do = True
    res = 0
    for inst in matches:
        if inst.startswith('mul'):
            a, b = inst.split('(')[1].split(',')
            if do: res += int(a) * int(b[:-1])
        elif inst.startswith('don\'t'):
            do = False
        elif inst.startswith('do'):
            do = True

    print('part2', res)

