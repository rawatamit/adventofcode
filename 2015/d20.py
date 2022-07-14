from aocd import get_data
import math


def divisors(n):
    m = int(math.sqrt(n) + 1)
    divs = []
    for i in range(1, m):
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
    return divs


def presents1(n):
    return sum(divisors(n)) * 10


def presents2(n):
    tot = 0
    for d in divisors(n):
        if d * 50 >= n:
            tot += d * 11
    return tot


if __name__ == '__main__':
    data = get_data(year=2015, day=20)
    num = int(data)

    # can't apply binary search, presents() is not monotonic
    n = 962499
    l = []
    for i in range(100000, n):
        tot_presents = presents1(i)
        if tot_presents >= num:
            print(tot_presents, i)
            break
