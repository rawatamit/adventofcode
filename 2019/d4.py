import itertools

num = 0


def two_adjacent_same(digits):
    for i in range(0, len(digits)-1):
        if digits[i] == digits[i+1]:
            return True
    return False

def no_decrease(digits):
    for i in range(0, len(digits)-1):
        if int(digits[i]) > int(digits[i+1]):
            return False
    return True

def any_digit_exactly_twice(digits):
    for _, x in itertools.groupby(digits):
        if len(list(x)) == 2:
            return True
    return False

def generate_num(digits, index):
    global num
    if index >= len(digits):
        if digits >= begin and digits <= upto and only_two_adjacent_same(digits):
            # print(digits, index)
            num += 1
    else:
        valid_digits = range(10) if index == 0 else range(digits[index - 1], 10)

        for digit in valid_digits:
            save = digits[index]
            digits[index] = digit
            generate_num(digits, index + 1)
            digits[index] = save

def part1(a, b):
    count = 0
    for i in range(a, b+1):
        digits = str(i)
        if two_adjacent_same(digits) and no_decrease(digits):
            count += 1
    print(count)

def part2(a, b):
    count = 0
    for i in range(a, b+1):
        digits = str(i)
        if two_adjacent_same(digits) and no_decrease(digits) and any_digit_exactly_twice(digits):
            count += 1
    print(count)

def main():
    #generate_num([1,3,0,2,5,4], 0)
    # part1(130254, 678275)
    part2(130254, 678275)

main()
