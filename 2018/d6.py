from collections import defaultdict


def grid_corners(coords):
    min_x = min(x for x,_ in coords)
    max_x = max(x for x,_ in coords)
    min_y = min(y for _,y in coords)
    max_y = max(y for _,y in coords)
    return (min_x, min_y), (max_x, max_y)


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def min_manhattan_distance(x, y, coords):
    dists = [((x2, y2), manhattan_distance(x, y, x2, y2))
            for x2, y2 in coords]
    
    sdists = sorted(dists, key=lambda x: x[1])
    # two equi distant points
    if sdists[0][1] == sdists[1][1]:
        return (None, None), None
    return sdists[0]


def compute_closest(min_x, max_x, min_y, max_y, coords):
    loc_closest = defaultdict(list)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            orig_coords, dist = min_manhattan_distance(x, y, coords)
            loc_closest[orig_coords].append(((x, y), dist))
    
    return loc_closest


def is_border(coords, nearest, min_x, max_x, min_y, max_y):
    border_fn = lambda x, y: x in (min_x, max_x) or y in (min_y, max_y)
    return border_fn(*coords) or any(border_fn(x, y) for (x, y), _ in nearest)


# part 2
def total_manhattan_distance(x, y, coords):
    return sum([manhattan_distance(x, y, x2, y2)
                for x2, y2 in coords])


def within_max_distance(min_x, max_x, min_y, max_y, coords, max_dist):
    within_region = []

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            dist = total_manhattan_distance(x, y, coords)
            if dist < max_dist:
                within_region.append((x, y))
    
    return within_region


if __name__ == '__main__':
    coords = []
    with open('d6.txt') as fin:
        for line in fin:
            x, y = [int(k) for k in line.split(',')]
            coords.append((x, y))
   
    # part 1
    (min_x, min_y), (max_x, max_y) = grid_corners(coords)
    loc_closest = compute_closest(min_x, max_x, min_y, max_y, coords)

    max_len = max(len(nearest)
                for (x, y), nearest in loc_closest.items()
                if not is_border((x, y), nearest, min_x, max_x, min_y, max_y))
    
    print(max_len)

    # part 2
    within_region = within_max_distance(min_x, max_x, min_y, max_y, coords, 10000)
    print(len(within_region))
