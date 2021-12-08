from aocd.models import Puzzle
from collections import Counter, defaultdict, namedtuple


def get_string_with_len(ips, slen):
    return [s for s in ips if len(s) == slen][0]


def has_seven(s, ips):
    tmp = get_string_with_len(ips, 3)
    return len(set(x for x in s if x in tmp)) == len(tmp)


def has_four(s, ips):
    tmp = get_string_with_len(ips, 4)
    return len(set(x for x in s if x in tmp)) == len(tmp)


def is_one(s, ips):
    return len(s) == 2


def is_four(s, ips):
    return len(s) == 4


def is_seven(s, ips):
    return len(s) == 3


def is_eight(s, ips):
    return len(s) == 7


# two, three, and five have five digits
# but only three has a seven embedded in it
def is_three(s, ips):
    return len(s) == 5 and has_seven(s, ips)


def has_three(s, ips):
    for ip in ips:
        if is_three(ip, ips):
            return len(set(x for x in s if x in ip)) == 5
    return False


# zero, nine and six have 6 segments
def is_zero(s, ips):
    return len(s) == 6 and has_seven(s, ips) and not has_four(s, ips)


def is_nine(s, ips):
    return len(s) == 6 and has_four(s, ips) and has_three(s, ips)


def is_six(s, ips):
    return len(s) == 6 and not has_seven(s, ips)


def is_five(s, ips):
    if has_seven(s, ips): return False

    for ip in ips:
        if is_six(ip, ips):
            return len(s) == 5 and len(set(ip) - set(s)) == 1
    return False 


def is_two(s, ips):
    return len(s) == 5 and not is_three(s, ips) and not is_five(s, ips)


def get_digit(s, ips):
    digmap = {0: is_zero, 1: is_one, 2: is_two,
              3: is_three, 4: is_four, 5: is_five,
              6: is_six, 7: is_seven, 8: is_eight,
              9: is_nine}
    
    for digit, fn in digmap.items():
        if fn(s, ips):
            return digit
    return -1


if __name__ == '__main__':
    Note = namedtuple('Note', ['input', 'output'])

    puzzle = Puzzle(year=2021, day=8)
    data = puzzle.input_data.split('\n')

    notes = []
    for row in data:
        ip, op = row.split('|')
        notes.append(Note(ip.split(), op.split()))
    
    diginum_map = {1: 2, 4: 4, 7: 3, 8: 7}
    digistr_map = {}

    total_dig_1478 = 0
    for note in notes:
        l = [x for x in note.output if len(x) in diginum_map.values()]
        total_dig_1478 += len(l)
    
    print(total_dig_1478)

    total_sum = 0
    for note in notes:
        num = ''.join(str(get_digit(op, note.input))
                      for op in note.output)
        total_sum += int(num)
    print(total_sum)
