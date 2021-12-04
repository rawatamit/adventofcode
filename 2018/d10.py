import re
from point import Point2D


class SkyObject:
    def __init__(self, pos, vel) -> None:
        self.pos = pos
        self.vel = vel
    
    def update(self):
        self.pos.add(self.vel)
    
    def reverse_update(self):
        subv = Point2D(-self.vel.x, -self.vel.y)
        self.pos.add(subv)

    def __str__(self) -> str:
        return f'SkyObject<position={self.pos}, velocity={self.vel}>'


def sky_bounds(objects):
    min_x = min(obj.pos.x for obj in objects)
    max_x = max(obj.pos.x for obj in objects)
    min_y = min(obj.pos.y for obj in objects)
    max_y = max(obj.pos.y for obj in objects)
    return min_x, max_x, min_y, max_y


def sky_area(objects):
    min_x, max_x, min_y, max_y = sky_bounds(objects)
    return abs(max_x - min_x) * abs(max_y - min_y)


def one_tick(objects):
    for obj in objects:
        obj.update()


def simulate_until_expansion(objects):
    last_area = float('inf')
    tick = 0

    while True:
        cur_area = sky_area(objects)
        if cur_area > last_area:
            print('nticks', tick - 1)
            for obj in objects: obj.reverse_update()
            break
        
        one_tick(objects)
        tick += 1
        last_area = cur_area
    
    draw_grid(objects)


def draw_grid(objects):
    min_x, max_x, min_y, max_y = sky_bounds(objects)

    grid = [['.' for _ in range(max_x + 1)]
            for _ in range(max_y + 1)]
    
    for obj in objects:
        grid[obj.pos.y][obj.pos.x] = '#'
    
    for row in grid:
        print(''.join(row))


if __name__ == '__main__':
    regex = r'position=<(?:\s+|)(-?\d+),(?:\s+|)(-?\d+)> velocity=<(?:\s+|)(-?\d+),(?:\s+|)(-?\d+)>'
    objects = []

    with open('d10.txt') as fin:
        for line in fin:
            if groups := re.search(regex, line):
                pos_x = int(groups.group(1))
                pos_y = int(groups.group(2))
                vel_x = int(groups.group(3))
                vel_y = int(groups.group(4))
                objects.append(SkyObject(Point2D(pos_x, pos_y), Point2D(vel_x, vel_y)))
    
    simulate_until_expansion(objects)
