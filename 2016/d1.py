import copy
from point import Point2D
import direction


def scalar_multiply(p, scalar):
    return Point2D(p.x * scalar, p.y * scalar)


def point_add(a, b):
    return Point2D(a.x + b.x, a.y + b.y)


def points_between(a, b, dir):
    cur = Point2D(a.x, a.y)

    while cur != b:
        next = point_add(cur, dir.offset)
        cur = next
        yield cur


if __name__ == '__main__':
    cur = Point2D(0, 0)
    dir = direction.North()
    seen = set()
    twice_visit = None

    with open('d1.txt') as fin:
        steps = fin.read().split(',')

        for step in steps:
            step = step.strip()

            if step[0] == 'L':
                dir = direction.turn_left(dir, 1)
            else:
                dir = direction.turn_right(dir, 1)

            forward = int(step[1:])

            orig = copy.deepcopy(cur)
            cur.add(scalar_multiply(dir.offset, forward))

            for p in points_between(orig, cur, dir):
                if p in seen and twice_visit is None:
                    twice_visit = p
                seen.add(p)
    
    print(cur.manhattan_distance(Point2D(0, 0)))
    print('twice', twice_visit, twice_visit.manhattan_distance(Point2D(0, 0)))
