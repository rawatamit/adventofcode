from aocd import get_data


def sum_digits(digits):
    return int(f'{digits[0]}{digits[-1]}')

def get_num_part1(line):
    digits = [x for x in line if x.isdigit()]
    return sum_digits(digits)

def get_num_part2(line):
    words = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
             'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
    digits = []
    for i,c in enumerate(line):
        if c.isdigit():
            digits.append(int(c))
        else:
            for k,v in words.items():
                if line[i:].startswith(k):
                    digits.append(v)
                    break
    return sum_digits(digits)


if __name__ == '__main__':
    data = """two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen"""
    data = get_data(year=2023, day=1)

    total = sum(get_num_part1(line.strip())
                for line in data.splitlines())
    print('part1', total)

    total = sum(get_num_part2(line.strip())
                for line in data.splitlines())
    print('part2', total)

