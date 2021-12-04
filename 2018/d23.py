import re
from point import Point3D
import z3


class Nanobot:
    def __init__(self, x, y, z, r) -> None:
        self.pos = Point3D(x, y, z)
        self.r = r
    
    def __str__(self) -> str:
        return f'Nanobot<position={self.pos}, radius={self.r}>'
    
    def distance_from(self, bot):
        return self.pos.manhattan_distance(bot.pos)
    
    def is_inrange(self, bot):
        return self.r >= self.distance_from(bot)


def in_range(bot, nanobots):
    return [nbot
            for nbot in nanobots
            if bot.is_inrange(nbot)]


# part 2
def abs_z3(x):
    return z3.If(x >= 0, x, -x)


def manhattan_distance(x1, y1, z1, x2, y2, z2):
    return abs_z3(x1 - x2) + abs_z3(y1 - y2) + abs_z3(z1 - z2)


def part2(nanobots):
    ## There is a point (x, y, z) in space which is closest to max number of
    ## bots. Even though there can be multiple of these, we need one of them.
    ## We ask Z3, if it can find a model of a point in 3D space, such that
    ## it is in range of maximum number of bots.
    solver = z3.Optimize()
    x = z3.Int('x')
    y = z3.Int('y')
    z = z3.Int('z')
    distance = z3.Int('distance')

    # assert distance as manhattan distance between (0,0,0) and (x,y,z)
    solver.add(distance == manhattan_distance(x, y, z, 0, 0, 0))

    bot_distances = []
    for i, bot in enumerate(nanobots):
        bot_z3 = z3.Int(f'b{i:4d}')
        ok = z3.If(manhattan_distance(x, y, z, bot.pos.x, bot.pos.y, bot.pos.z) <= bot.r, 1, 0)
        solver.add(ok == bot_z3)
        bot_distances.append(bot_z3)

    solver.maximize(z3.Sum(*bot_distances))
    solver.minimize(distance)
    solver.check()
    m = solver.model()
    return m.eval(distance)


if __name__ == '__main__':
    regex = r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)'
    bots = []

    with open('d23.txt') as fin:
        for line in fin:
            if groups := re.search(regex, line):
                x = int(groups.group(1))
                y = int(groups.group(2))
                z = int(groups.group(3))
                r = int(groups.group(4))
                bots.append(Nanobot(x, y, z, r))

    # part 1
    bot_largest_r = sorted(bots, key=lambda bot: bot.r)[-1]
    print(len(in_range(bot_largest_r, bots)))

    print(part2(bots))
