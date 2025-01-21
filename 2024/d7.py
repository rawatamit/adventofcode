from aocd import get_data
import math


def solve(nums, ops):
    res = 0
    for i, x in enumerate(nums):
        # no op for first number
        if i == 0:
            res = x
        elif ops[i-1] == '*':
            res *= x
        elif ops[i-1] == '+':
            res += x
        elif ops[i-1] == '||':
            ndigits = int(math.log10(x)) + 1
            res = (10 ** ndigits) * res + x
    return res


def gen(res, nums, ops, i, allops):
    nops = len(nums) - 1
    # ops only go between numbers. check if this is equal to the result
    if len(ops) == nops:
        return solve(nums, ops) == res

    for j in range(i, nops):
        for op in allops:
            ops.append(op)
            if gen(res, nums, ops, j+1, allops):
                return True
            ops.pop()

    return False


def part1(res, nums):
    return gen(res, nums, [], 0, ('*', '+'))


def part2(res, nums):
    return gen(res, nums, [], 0, ('*', '+', '||'))


if __name__ == '__main__':
    data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
    data = get_data(year=2024, day=7)

    total_cal = 0
    for line in data.split('\n'):
        res, nums = line.split(':')
        res = int(res)
        nums = [int(x) for x in nums.split()]
        istrue = part1(res, nums) 
        total_cal += res if istrue else 0

    print('part1', total_cal)

    total_cal = 0
    for line in data.split('\n'):
        res, nums = line.split(':')
        res = int(res)
        nums = [int(x) for x in nums.split()]
        istrue = part2(res, nums) 
        total_cal += res if istrue else 0
    print('part2', total_cal)

