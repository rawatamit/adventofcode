def find(nums, s, e, x):
    for i in range(s, e+1):
        if nums[i] == x:
            return True
    return False


# sum of two numbers that sum to nums[i]
# where preamble length is specified
def find_sum(nums, i, preamble_len):
    s, e = i - preamble_len, i - 1
    n = nums[i]
    for j in range(s, e+1):
        a = nums[j]
        if find(nums, j + 1, e, n - a):
            return a, n - a
    return -1, -1


def first_not_sum(nums, preamble_len=25):
    for i in range(preamble_len, len(nums)):
        a, b = find_sum(nums, i, preamble_len)
        if a == -1 and b == -1:
            return nums[i]


def find_sum(nums, x):
    s, e = 0, 0
    cursum = nums[s]
    while e < len(nums):
        if cursum == x and e > s:
            return sorted(nums[s:e+1])

        e += 1
        cursum += nums[e]
        while cursum > x:
            cursum -= nums[s]
            s += 1


if __name__ == "__main__":
    with open('d9.txt') as fin:
        nums = [int(x) for x in fin.readlines()]
    #x = first_not_sum(nums)
    #print(x)
    x = find_sum(nums, 542529149)
    print(x, x[0] + x[-1])
