from itertools import product
from collections import defaultdict
import copy


class Point3D:
    def __init__(self, x, y, z) -> None:
        self.coordinates = [x, y, z]
        self.n = 3
    
    def __str__(self) -> str:
        return f'Point3D({self.x}, {self.y}, {self.z})'
    
    def __eq__(self, o: object) -> bool:
        return o is not None and self.coordinates == o.coordinates
    
    def __hash__(self) -> int:
        return 23 + sum(self.coordinates[i] * (3,7,11)[i]
                        for i in range(self.n))

    @property
    def x(self): return self.coordinates[0]

    @property
    def y(self): return self.coordinates[1]

    @property
    def z(self): return self.coordinates[2]

    def add(self, o):
        for i in range(self.n):
            self.coordinates[i] += o.coordinates[i]
    
    def neighbors(self):
        for dx, dy, dz in product((-1, 0, +1), repeat=3):
            if (dx, dy, dz) != (0, 0, 0):
                yield Point3D(self.x + dx, self.y + dy, self.z + dz)
 

class Point4D:
    def __init__(self, x, y, z, w) -> None:
        self.coordinates = [x, y, z, w]
        self.n = 4
    
    def __str__(self) -> str:
        return f'Point4D({self.x}, {self.y}, {self.z}, {self.w})'
    
    def __eq__(self, o: object) -> bool:
        return o is not None and self.coordinates == o.coordinates
    
    def __hash__(self) -> int:
        return 23 + sum(self.coordinates[i] * (3,7,11,17)[i]
                        for i in range(self.n))

    @property
    def x(self): return self.coordinates[0]

    @property
    def y(self): return self.coordinates[1]

    @property
    def z(self): return self.coordinates[2]

    @property
    def w(self): return self.coordinates[3]

    def add(self, o):
        for i in range(self.n):
            self.coordinates[i] += o.coordinates[i]
    
    def neighbors(self):
        for dx, dy, dz, dw in product((-1, 0, +1), repeat=4):
            if (dx, dy, dz, dw) != (0, 0, 0, 0):
                yield Point4D(self.x + dx, self.y + dy, self.z + dz, self.w + dw)
 

def is_active(grid, cube):
    return grid.get(cube, '.') == '#'


def num_active(grid, cube):
    return sum(1 for ncube in cube.neighbors() if is_active(grid, ncube))


def add_neigbors(grid, cube):
    for ncube in cube.neighbors():
        if ncube not in grid:
            grid[ncube] = '.'


def one_cycle(grid):
    new_grid = {}
    for cube, state in grid.items():
        new_grid[cube] = state
        add_neigbors(new_grid, cube)

    tmp_grid = {}

    for cube in new_grid.keys():
        # find number of active from new_grid
        # as cubes may be added to it, and we don't
        # want to change the grid keys
        nactive = num_active(new_grid, cube)

        if is_active(new_grid, cube):
            tmp_grid[cube] = '#' if nactive in (2, 3) else '.'
        else:
            tmp_grid[cube] = '#' if nactive == 3 else '.'
     
    for cube, state in tmp_grid.items():
        new_grid[cube] = state
    return new_grid


def ncycle(grid, n=1):
    for _ in range(n):
        grid = one_cycle(grid)
    return grid


def draw_same_z(grid, cubes):
    max_x = max(cube.x for cube in cubes)
    max_y = max(cube.y for cube in cubes)
    min_x = min(cube.x for cube in cubes)
    min_y = min(cube.y for cube in cubes)

    min_x, min_y = abs(min_x), abs(min_y)

    buffer = [['.' for _ in range(max_y+min_y+1)]
              for _ in range(max_x+min_x+1)]

    for cube in cubes:
        buffer[min_x + cube.x][min_y + cube.y] = grid[cube]
    
    for row in buffer:
        print(''.join(row))


def draw(grid):
    same_z = defaultdict(list)

    for cube in grid.keys():
        same_z[cube.z].append(cube)
    
    for z, cubes in same_z.items():
        print(f'z={z}')
        draw_same_z(grid, cubes)


def part1():
    grid = {}

    with open('d17.txt') as fin:
        row = 0
        for line in fin:
            for col, state in enumerate(line.strip()):
                cube = Point3D(row, col, z=0)
                grid[cube] = state
            row += 1
    
    grid = ncycle(grid, n=6)
    total_active = sum(1 for cube in grid.keys() if grid[cube] == '#')
    print(total_active)


def part2():
    grid = {}

    with open('d17.txt') as fin:
        row = 0
        for line in fin:
            for col, state in enumerate(line.strip()):
                cube = Point4D(row, col, z=0, w=0)
                grid[cube] = state
            row += 1
    
    grid = ncycle(grid, n=6)
    total_active = sum(1 for cube in grid.keys() if grid[cube] == '#')
    print(total_active)


def main():
    #part1()
    part2()


main()
