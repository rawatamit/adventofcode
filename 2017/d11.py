class Cube:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self) -> str:
        return f'Cube({self.x},{self.y},{self.z})'


def add_cube(a, b):
    return Cube(a.x+b.x, a.y+b.y, a.z+b.z)


def distance(a, b):
    return max(abs(a.x - b.x), abs(a.y - b.y), abs(a.z - b.z))


def neigbor(cube, dir):
    dirmap = {'se': Cube(+1, -1, 0), 's': Cube(0, -1, +1), 'sw': Cube(-1, 0, +1),
              'nw': Cube(-1, +1, 0), 'n': Cube(0, +1, -1), 'ne': Cube(+1, 0, -1)}
    
    return add_cube(cube, dirmap[dir])


def part12(cube, dirs):
    ncube = cube
    max_dist = -1

    for dir in dirs:
        ncube = neigbor(ncube, dir)
        max_dist = max(max_dist, distance(ncube, cube))

    return distance(ncube, cube), max_dist


def main():
    with open('d11.txt') as fin:
        dirs = fin.read().strip().split(',')

    dist_end, max_dist = part12(Cube(0, 0, 0), dirs)
    print(dist_end, max_dist)


main()
