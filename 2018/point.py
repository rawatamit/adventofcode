from itertools import product


class Point2D:
    def __init__(self, x, y) -> None:
        self.coordinates = [x, y]
        self.n = 2
    
    def __str__(self) -> str:
        return f'Point2D({self.x}, {self.y})'
    
    def __eq__(self, o: object) -> bool:
        return o is not None and self.coordinates == o.coordinates
    
    def __hash__(self) -> int:
        return 23 + sum(self.coordinates[i] * (3,7)[i]
                        for i in range(self.n))

    @property
    def x(self): return self.coordinates[0]

    @property
    def y(self): return self.coordinates[1]

    def rotate_left(self):
        self.coordinates = [self.y, -self.x]

    def rotate_right(self):
        self.coordinates = [-self.y, self.x]

    def add(self, o):
        for i in range(self.n):
            self.coordinates[i] += o.coordinates[i]

    def manhattan_distance(self, o):
        return sum(abs(self.coordinates[i] - o.coordinates[i])
                   for i in range(self.n))


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
    
    def manhattan_distance(self, o):
        return sum(abs(self.coordinates[i] - o.coordinates[i])
                   for i in range(self.n))
