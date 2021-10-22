import copy


class Vector3D:
    def __init__(self, x, y, z) -> None:
        self.coordinates = [x, y, z]
        self.n = len(self.coordinates)
    
    def __str__(self) -> str:
        return f'Vector3D{self.coordinates}'
    
    def __eq__(self, o: object) -> bool:
        if o is None or not isinstance(o, Vector3D):
            return False
        return self.coordinates == o.coordinates
    
    @property
    def x(self):
        return self.coordinates[0]

    @property
    def y(self):
        return self.coordinates[1]

    @property
    def z(self):
        return self.coordinates[2]
    
    def add(self, other):
        assert isinstance(other, Vector3D)
        for i in range(self.n):
            self.coordinates[i] += other.coordinates[i]
    
    def manhattan_distance(self, other):
        return sum(abs(self.coordinates[i] - other.coordinates[i])
                    for i in range(self.n))


class Point:
    def __init__(self, pos, vel, acc) -> None:
        self.pos = pos
        self.vel = vel
        self.acc = acc
    
    def __str__(self) -> str:
        return f'Point(pos={self.pos}, vel={self.vel}, acc={self.acc})'
    
    def update(self):
        self.vel.add(self.acc)
        self.pos.add(self.vel)
    
    def manhattan_distance(self, other):
        return self.pos.manhattan_distance(other)


def one_tick(points):
    for point in points:
        point.update()


def part1(points):
    points = copy.deepcopy(points)
    origin = Vector3D(0, 0, 0)

    for i in range(1000):
        one_tick(points)

    ds = [point.manhattan_distance(origin) for point in points]
    min_d = min(ds)
    return ds.index(min_d)


def part2(points):
    spoints = copy.deepcopy(points)

    for _ in range(900):
        one_tick(spoints)

        delete_set = set()
        for i in range(len(spoints)):
            for j in range(i+1, len(spoints)):
                if spoints[i].pos == spoints[j].pos:
                    delete_set.add(i)
                    delete_set.add(j)
        
        spoints = [spoints[i]
                   for i in range(len(spoints))
                   if i not in delete_set]
    
    return spoints


def read_point(s):
    pos, vel, acc = s.split('>,')
    pos, vel, acc = pos.strip()[3:], vel.strip()[3:], acc.strip()[3:-1]
    pos = Vector3D(*[int(x) for x in pos.split(',')])
    vel = Vector3D(*[int(x) for x in vel.split(',')])
    acc = Vector3D(*[int(x) for x in acc.split(',')])
    return Point(pos, vel,acc)


def main():
    points = []
    with open('d20.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                point = read_point(line)
                points.append(point)
    
    # part 1
    # pindex = part1(points)
    # print(f'closest {pindex}')

    # part 2
    spoints = part2(points)
    #for p in spoints: print(p)
    print(len(spoints))


main()
