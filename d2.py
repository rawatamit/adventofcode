def parse_policy(line):
    bounds, letter, passwd = line.strip().split()
    a, b = bounds.split('-')
    return range(int(a), int(b)+1), letter.strip()[:-1], passwd.strip()


def is_valid1(bounds, letter, passwd):
    return passwd.count(letter) in list(bounds)

def is_valid2(bounds, letter, passwd):
    positions = list(bounds)
    a, b = positions[0] - 1, positions[-1] - 1
    match = 0
    if passwd[a] == letter:
        match += 1
    if passwd[b] == letter:
        match += 1
    return match == 1

def valid_passwds(policies):
    count = 0
    for line in policies:
        bounds, letter, passwd = parse_policy(line)
        if is_valid2(bounds, letter, passwd):
            count += 1
    return count


if __name__ == '__main__':
    with open('d2.txt') as fin:
        policies = fin.readlines()
    v = valid_passwds(policies)
    print(v)
