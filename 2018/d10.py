from vector import Vector2D


class Point:
    def __init__(self, pos, vel) -> None:
        self.pos = pos
        self.vel = vel
    
    def __repr__(self) -> str:
        return str(self)
    
    def __str__(self) -> str:
        return f'Point(pos={self.pos}, vel={self.vel})'


def parse_point(s):
    # position=< 9,  1> velocity=< 0,  2>
    pos, vel = s.split('> velocity=<')
    pos = [int(x) for x in pos.split('position=<')[1].split(',')]
    vel = [int(x) for x in vel[:-1].split(',')]

    return Point(Vector2D(pos), Vector2D(vel))


def draw(points):
    min_x = min(point.pos.x for point in points)
    max_x = max(point.pos.x for point in points)
    min_y = min(point.pos.y for point in points)
    max_y = max(point.pos.y for point in points)

    rows = abs(max_y) - abs(min_y)
    cols = abs(max_x) - abs(min_x)

    grid = [['.' for _ in range(cols+1)] for _ in range(rows+1)]

    for point in points:
        x = point.pos.x - min_x
        y = point.pos.y - min_y
        print((x, y), point.pos, (min_x, min_y), (max_x, max_y))
        grid[y][x] = '#'
    
    for row in grid:
        print(''.join(row))


def part1(points):
    count = 0
    for _ in range(100):
        count += 1
        if count == 5:
            count = 0
            draw(points)
            print()

        for point in points:
            point.pos.move_vector(point.vel)


def main():
    points = []
    with open('d10.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                points.append(parse_point(line))
    
    # part 1
    #print(points)
    part1(points)

main()
