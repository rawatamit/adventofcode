from aocd.models import Puzzle
import re
import string


def groups_of(s, n=1):
    i = 0
    while i+n <= len(s):
        yield s[i:i+n]
        i += 1


def is_password(s):
    combs = groups_of(string.ascii_lowercase, 3)
    if re.search('[iol]', s):
        return False
    
    if any(re.search(comb, s) for comb in combs):
        return re.search(r'(\w)\1{1}.*(\w)\2{1}', s)


def next_string(s):
    lwcase = string.ascii_lowercase
    next_c = {c: n for c, n in zip(lwcase, lwcase[1:])}

    # skip i, o, l
    next_c['h'] = next_c['i']
    next_c['n'] = next_c['o']
    next_c['k'] = next_c['l']

    next_c['z'] = 'a'

    new_s = [c for c in s]
    i = len(s) - 1
    while new_s[i] == 'z':
        new_s[i] = next_c['z']
        i -= 1
    
    new_s[i] = next_c[new_s[i]]
    return ''.join(new_s)


def next_password(s):
    s = next_string(s)
    while not is_password(s):
        s = next_string(s)
    return s


if __name__ == '__main__':
    puzzle = Puzzle(year=2015, day=11)

    data = 'ghijklmn'
    data = puzzle.input_data

    part_1 = next_password(data)

    print(part_1)
    print(next_password(part_1))
