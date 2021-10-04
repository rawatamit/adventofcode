import math

def tuple_add(ta, tb):
    assert len(ta) == len(tb)
    return tuple(ta[i] + tb[i] for i in range(len(ta)))

def tuple_subtract(ta, tb):
    assert len(ta) == len(tb)
    return tuple(ta[i] - tb[i] for i in range(len(ta)))

class Vector3D:
    def __init__(self, *args) -> None:
        assert len(args) == 3
        self.contents = args
    
    def __len__(self):
        return len(self.contents)
    
    def __getitem__(self, i):
        assert 0 <= i < len(self)
        return self.contents[i]

    def add(self, v):
        assert isinstance(v, Vector3D)
        self.contents = tuple_add(self.contents, v)
    
    def diff(self, v):
        assert isinstance(v, Vector3D)
        fn = lambda x: -1 if x < 0 else (+1 if x > 0 else 0)
        x, y, z = tuple_subtract(self.contents, v.contents)
        return Vector3D(fn(x), fn(y), fn(z))
    
    @property
    def x(self):
        return self.contents[0]
    
    @property
    def y(self):
        return self.contents[1]

    @property
    def z(self):
        return self.contents[2]
    
    def __iter__(self):
        for i in range(len(self.contents)):
            yield self[i]
    
    def __eq__(self, o: object) -> bool:
        if self is o: return True
        return self.contents == o.contents
    
    def __repr__(self) -> str:
        return f'Vector3D({self.x}, {self.y}, {self.z})'

class Moon:
    def __init__(self, x, y, z) -> None:
        self.pos = Vector3D(x, y, z)
        self.vel = Vector3D(0, 0, 0)
    
    def __eq__(self, o: object) -> bool:
        if o is self: return True
        return self.pos == o.pos and self.vel == o.vel
    
    def apply_gravity(self, moon):
        self.vel.add(moon.pos.diff(self.pos))

    def apply_velocity(self):
        self.pos.add(self.vel)
    
    @property
    def potential_energy(self):
        return sum(abs(x) for x in self.pos)
    
    @property
    def kinetic_energy(self):
        return sum(abs(x) for x in self.vel)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        pos_s = f"pos=<x={self.pos.x}, y={self.pos.y}, z={self.pos.z}>"
        vel_s = f"vel=<x={self.vel.x}, y={self.vel.y}, z={self.vel.z}>"
        return f'{pos_s}, {vel_s}'


def read_moon(s):
    moon_pos = {}
    for dim_pos in s[1:-1].split(','):
        dim, pos = dim_pos.strip().split('=')
        moon_pos[dim] = int(pos)
    return Moon(moon_pos['x'], moon_pos['y'], moon_pos['z'])


def pairwise_gravity(this_moon, moons):
    for moon in moons:
        if this_moon != moon:
            this_moon.apply_gravity(moon)


def time_step(moons):
    for moon in moons:
        pairwise_gravity(moon, moons)
    for moon in moons:
        moon.apply_velocity()


def time_steps(moons, steps):
    for i in range(steps):
        time_step(moons)


def total_energy(moons):
    pot_energy = 0
    for moon in moons:
        pot_energy += moon.potential_energy * moon.kinetic_energy
    return pot_energy


def partial_state(moons, fn):
    return [fn(moon) for moon in moons]


def lcm(x, y):
    return (x * y) // math.gcd(x, y)


def part2(moons):
    fn_x = lambda moon: (moon.pos.x, moon.vel.x)
    fn_y = lambda moon: (moon.pos.y, moon.vel.y)
    fn_z = lambda moon: (moon.pos.z, moon.vel.z)

    start_x = partial_state(moons, fn_x)
    start_y = partial_state(moons, fn_y)
    start_z = partial_state(moons, fn_z)

    repeat_x = None
    repeat_y = None
    repeat_z = None

    step = 0
    while repeat_x is None or repeat_y is None or repeat_z is None:
        time_step(moons)
        step += 1

        repeat_x = step if repeat_x is None and partial_state(moons, fn_x) == start_x else repeat_x
        repeat_y = step if repeat_y is None and partial_state(moons, fn_y) == start_y else repeat_y
        repeat_z = step if repeat_z is None and partial_state(moons, fn_z) == start_z else repeat_z
    
    return lcm(repeat_x, lcm(repeat_y, repeat_z))


def main():
    moons = []
    with open('d12.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                moons.append(read_moon(line))
    
    ## part 1
    # time_steps(moons, 1000)
    # print(total_energy(moons))

    ## part 2
    x = part2(moons)
    print(x)

main()
