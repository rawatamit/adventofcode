def components(s):
    return s.split(',')


def cycle(x):
    while True:
        yield x


def update_points(i1, i2, dist, cur_dist):
    res = []

    for xi, yi in zip(i1, i2):
        dist[(xi, yi)] = cur_dist
        cur_dist += 1
        res.append((xi, yi))

    return res


def get_points(path):
    x, y = 0, 0
    cur_dist = 0
    dist = {(x, y): 0}
    points = []

    for p in path:
        cmd, d = p[0], int(p[1:])
        if cmd == 'R':
            points.extend(update_points(range(x, x+d), cycle(y), dist, cur_dist))
            cur_dist = dist[(x+d-1, y)] + 1
            x = x + d
        elif cmd == 'L':
            points.extend(update_points(range(x, x-d, -1), cycle(y), dist, cur_dist))
            cur_dist = dist[(x-d+1, y)] + 1
            x = x - d
        elif cmd == 'U':
            points.extend(update_points(cycle(x), range(y, y+d), dist, cur_dist))
            cur_dist = dist[(x, y+d-1)] + 1
            y = y + d
        elif cmd == 'D':
            points.extend(update_points(cycle(x), range(y, y-d, -1), dist, cur_dist))
            cur_dist = dist[(x, y-d+1)] + 1
            y = y - d
    
    return dist, set(points)


def intersection(dist1, dist2, points1, points2):
    res = []

    for k in points1:
        if k in points2:
            res.append((k, dist1[k] + dist2[k]))
    return res


def closest_to_central_part1(int_points):
    x, y = 0, 0
    for (xi, yi), d in int_points:
        if (x, y) == (0, 0):
            x, y = xi, yi

        if (xi, yi) != (0, 0):
            if abs(xi) + abs(yi) < abs(x) + abs(y):
                x, y = xi, yi
    return x, y


def closest_to_central_part2(int_points):
    x, y, d = 0, 0, 0
    for (xi, yi), di in int_points:
        if (x, y) == (0, 0):
            x, y, d = xi, yi, di

        if (xi, yi) != (0, 0):
            if di < d:
                x, y, d = xi, yi, di
    return x, y, d


def main():
    with open('d3.txt') as fin:
        s1 = fin.readline().strip()
        s2 = fin.readline().strip()

    path1 = components('R8,U5,L5,D3')
    path2 = components('U7,R6,D4,L4')
    
    # path1 = components('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51')
    # path2 = components('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7')

    path1 = components(s1)
    path2 = components(s2)

    dist1, points1 = get_points(path1)
    dist2, points2 = get_points(path2)
    
    #print(points1, points2)

    int_points = intersection(dist1, dist2, points1, points2)
    x, y, d = closest_to_central_part2(int_points)
    print(x, y, d)

main()
