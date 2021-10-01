import math
import itertools
from collections import defaultdict

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f'Point2D({self.x},{self.y})'

    def __repr__(self):
        return f'Point2D({self.x},{self.y})'
    
    def __eq__(self, point):
        return self.x == point.x and self.y == point.y
    
    def angle_to(self, point):
        rads = math.atan2(point.y - self.y, point.x - self.x)
        degs = math.degrees(rads) + 90
        return (degs + 360) if degs < 0 else degs

def find_angles_relative(point, points):
    return [point.angle_to(p) for p in points if p != point]

def find_angles_relative2(point, points):
    return [(p, point.angle_to(p)) for p in points if p != point]

def euclidean_distance(pa, pb):
    return math.sqrt((pa.x - pb.x) **2 + (pa.y - pb.y) ** 2)

def manhattan_distance(pa, pb):
    return abs(pa.x - pb.x) + abs(pa.y - pb.y)

def main():
    points = []
    with open('d10.txt') as fin:
        y = 0
        for line in fin:
            line = line.strip()
            for x in range(len(line)):
                if line[x] == '#':
                    points.append(Point2D(x, y))
            y += 1

    ## part 1
    # max_p = 0
    # for p in points:
    #     l = find_angles_relative(p, points)
    #     max_p = max(max_p, len(set(l)))
    
    # print(max_p)

    ## part 2
    max_p = 0
    max_point = None
    max_pa = None

    for p in points:
        l = find_angles_relative2(p, points)
        only_angles = [angle for _, angle in l]
        unique_angles = len(set(only_angles))

        if len(set(only_angles)) > max_p:
            max_p = unique_angles
            max_point = p
            max_pa = l
    
    # group_fn = lambda x: x[1] # group by angle
    # groups = itertools.groupby(max_pa, key=group_fn)
    # then sort by euclidean distacne
    sort_fn = lambda x: euclidean_distance(max_point, x)
    groups = defaultdict(list)

    for point, angle in max_pa:
        groups[angle].append(point)
    
    processed = []
    for k, v in groups.items():
        processed.append((k, sorted(v, key=sort_fn, reverse=True)))
    processed.sort(key=lambda x: x[0])

    # for k, v in processed:
    #     print(k, v)

    i, j = 0, 0
    while i < 200:
        if len(processed[j][1]) > 0:
            point = processed[j][1].pop()
            print(processed[j][0], point)
        j += 1
        if j >= len(processed): j = 0
        i += 1

main()
