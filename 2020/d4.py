import re


def read_passport(stream):
    passport = []
    for line in stream:
        line = line.strip()
        if line:
            passport.append(line)
        else:
            break
    return passport


def extract_fields(passport):
    fields = {}
    for data in passport:
        fields.update(x.split(':') for x in data.split())
    return fields


def check_passport_field(field, value):
    def in_range(s, a, b):
        return a <= int(s) <= b

    def height(s):
        if s.endswith('cm'):
            return in_range(s[:-2], 150, 193)
        if s.endswith('in'):
            return in_range(s[:-2], 59, 76)

    def hair_color(s):
        return re.match('^#[a-f0-9]{6}$', s) is not None
    
    def passport_id(s):
        return re.match('^[0-9]{9}$', s) is not None
    
    ecl = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
    fns = {'byr': lambda s: in_range(s, 1920, 2002),
           'iyr': lambda s: in_range(s, 2010, 2020),
           'eyr': lambda s: in_range(s, 2020, 2030),
           'hgt': height,
           'hcl': hair_color,
           'ecl': lambda s: s in ecl,
           'pid': passport_id,
           'cid': lambda s: True}
    return fns[field](value)


def check_passport_fields(passport):
    return all([check_passport_field(k, v)
        for k,v in passport.items()])


def is_valid_passport(passport):
    expected_fields1 = sorted(['byr', 'iyr', 'eyr',
        'hgt', 'hcl', 'ecl', 'pid'])
    expected_fields2 = sorted(expected_fields1 + ['cid'])
    return ((sorted(passport.keys()) == expected_fields1
         or sorted(passport.keys()) == expected_fields2)
         and check_passport_fields(passport))


def all_passports(stream):
    while True:
        passport = read_passport(stream)
        if passport:
            fields = extract_fields(passport)
            yield fields
        else:
            break


def valid_passports(stream):
    return filter(is_valid_passport, all_passports(stream))


if __name__ == '__main__':
    with open('d4.txt') as fin:
        x = list(valid_passports(fin))
        print(len(x))
