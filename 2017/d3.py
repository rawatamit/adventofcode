import math


def coordinates(n):
    # from OEIS.org

    # x coordinate
    # a(1) = 0, a(n) = a(n-1) + sin(floor(sqrt(4 * (n - 2) + 1)) % 4) *pi/2)

    # y coordinate
    # a(1) = 0, a(n) = a(n-1) - cos(floor(sqrt(4 * (n - 2) + 1)) % 4) * pi/2)

    x = 0
    y = 0
    for k in range(2, n+1):
        rads = math.floor(math.sqrt(4 * (k - 2) + 1)) % 4
        x = x + math.sin(rads * math.pi / 2)
        y = y - math.cos(rads * math.pi / 2)
    
    return x, y


def main():
    # part 1
    x, y = coordinates(289326)
    print(abs(x) + abs(y))

    # part 2
    # http://oeis.org/A141481

main()
