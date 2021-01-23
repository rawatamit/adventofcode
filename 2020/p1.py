def p1(nums):
    for i in range(len(nums)):
        a = nums[i]
        if (2020-a) in nums[i+1:]:
            return a, 2020-a


def p2(nums):
    for i in range(len(nums)):
        a = nums[i]
        for j in range(i+1, len(nums)):
            b = nums[j]
            if (2020-a-b) in nums[j+1:]:
                return a * b * (2020-a-b)


if __name__ == '__main__':
    with open('p1.txt') as fin:
        nums = [int(x) for x in fin.readlines()]
    v = p2(nums)
    print(v)
