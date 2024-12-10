from aocd import get_data
from collections import Counter

if __name__ == '__main__':
    data = """3   4
4   3
2   5
1   3
3   9
3   3"""
    data = get_data(year=2024, day=1)
    left = []
    right = []
    for line in data.split('\n'):
        a, b = line.split()
        left.append(int(a))
        right.append(int(b))
    left.sort()
    right.sort()
    s = 0
    for i in range(len(left)):
        s += abs(left[i] - right[i])
    print('part1', s)

    sim = 0
    rightf = Counter(right)
    for x in left:
        sim += x * rightf.get(x, 0)
    print('part2', sim)
