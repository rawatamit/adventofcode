def add_cube(a, b):
    return Cube(a.q + b.q, a.r + b.r, a.s + b.s)


class Cube:
    def __init__(self, q, r, s) -> None:
        self.q = q
        self.r = r
        self.s = s
   
    def __str__(self) -> str:
        return f'Cube({self.q}, {self.r}, {self.s})'
    
    def __eq__(self, o: object) -> bool:
        return (o is not None and
                isinstance(o, Cube) and
                (self.q, self.r, self.s) == (o.q, o.r, o.s))
    
    def __hash__(self) -> int:
        return 23 + 3 * self.q + 7 * self.r + 11 * self.s
    
    def neigbor(self, dir):
        neigbor_offset = {'e': Cube(+1, 0, -1), 'ne': Cube(+1, -1, 0),
                          'nw': Cube(0, -1, +1), 'w': Cube(-1, 0, +1),
                          'sw': Cube(-1, +1, 0), 'se': Cube(0, +1, -1)}
 
        offset = neigbor_offset[dir]
        return add_cube(self, offset)
    
    def neigbors(self):
        for dir in ('e', 'ne', 'nw', 'w', 'sw', 'se'):
            yield self.neigbor(dir)


def get_color(cubes, cube):
    return cubes.get(cube, 'W')


def walk(cubes, init_cube, path):
    i = 0
    cube = init_cube
    flip_color = {'B': 'W', 'W': 'B'}

    # walk the path, but don't flip the colors
    while i < len(path):
        # cube is not in path, add it with white color by default
        if cube not in cubes:
            cubes[cube] = 'W'
        
        if path[i] in ('n', 's'):
            dir = path[i:i+2]
            i += 2 
        else:
            dir = path[i]
            i += 1
        
        cube = cube.neigbor(dir)
    
    # flip color of the last cube
    cubes[cube] = flip_color[get_color(cubes, cube)]


def part1():
    init_cube = Cube(0, 0, 0)
    cubes = {}

    with open('d24.txt') as fin:
        for line in fin:
            line = line.strip()
            if line: walk(cubes, init_cube, line)

    # count black cubes
    return sum(1 for color in cubes.values() if color == 'B')


def simulate(cubes):
    flip_cubes = set()
    flip_color = {'B': 'W', 'W': 'B'}

    new_cubes = [ncube for cube in cubes.keys()
                for ncube in cube.neigbors()
                if ncube not in cubes]
    
    for cube in new_cubes:
        cubes[cube] = 'W'
     
    for cube, color in cubes.items():
        nblack = sum(1 for cube in cube.neigbors()
                        if cube in cubes and cubes[cube] == 'B')
        
        if color == 'B' and (nblack == 0 or nblack > 2):
            flip_cubes.add(cube)
        elif color == 'W' and nblack == 2:
            flip_cubes.add(cube)
    
    for cube in flip_cubes:
        cubes[cube] = flip_color[get_color(cubes, cube)]


def part2(ndays=1):
    init_cube = Cube(0, 0, 0)
    cubes = {}
    paths = []

    with open('d24.txt') as fin:
        for line in fin:
            line = line.strip()
            if line: paths.append(line)
    
    for path in paths:
        walk(cubes, init_cube, path)
    
    for _ in range(ndays):
        simulate(cubes)

    # count black cubes
    return sum(1 for color in cubes.values() if color == 'B')


if __name__ == '__main__':
    print(part1())
    print(part2(ndays=100))
