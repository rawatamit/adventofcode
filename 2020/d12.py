from point import Point2D
import direction


def scalar_multiply_point(a, scalar):
    return Point2D(a.x * scalar, a.y * scalar)


class Ship:
    def __init__(self, pos, dir) -> None:
        self.pos = pos
        self.dir = dir
    
    def move_in_direction(self, dir, value):
        self.move_towards(dir.offset, value)

    def move_forward(self, value):
        self.move_in_direction(self.dir, value)

    def move_towards(self, point, value):
        move_vector = scalar_multiply_point(point, value)
        self.pos.add(move_vector)

    def turn_left(self, degrees):
        self.dir = direction.turn_left(self.dir, degrees // 90)

    def turn_right(self, degrees):
        self.dir = direction.turn_right(self.dir, degrees // 90)


class Waypoint:
    def __init__(self, pos) -> None:
        self.pos = pos
    
    def rotate_left(self, degrees):
        for _ in range(degrees // 90):
            self.pos.rotate_left()

    def rotate_right(self, degrees):
        for _ in range(degrees // 90):
            self.pos.rotate_right()

    def move_in_direction(self, dir, value):
        move_vector = scalar_multiply_point(dir.offset, value)
        self.pos.add(move_vector)


def part1():
    ship = Ship(pos=Point2D(0, 0), dir=direction.East())

    with open('d12.txt') as fin:
        for line in fin:
            line = line.strip()
            cmd, value = line[0], int(line[1:])

            if cmd == 'F':
                ship.move_forward(value)
            elif cmd == 'L':
                ship.turn_left(value)
            elif cmd == 'R':
                ship.turn_right(value)
            elif cmd == 'N':
                ship.move_in_direction(direction.North(), value)
            elif cmd == 'S':
                ship.move_in_direction(direction.South(), value)
            elif cmd == 'E':
                ship.move_in_direction(direction.East(), value)
            elif cmd == 'W':
                ship.move_in_direction(direction.West(), value)

    print(ship.pos.manhattan_distance(Point2D(0, 0)))


def part2():
    ship = Ship(pos=Point2D(0, 0), dir=direction.East())

    wp_init_pos = scalar_multiply_point(direction.East().offset, 10)
    wp_init_pos.add(direction.North().offset)
    waypoint = Waypoint(wp_init_pos)

    with open('d12.txt') as fin:
        for line in fin:
            line = line.strip()
            cmd, value = line[0], int(line[1:])

            if cmd == 'F':
                #print(ship.pos, waypoint.pos)
                ship.move_towards(waypoint.pos, value)
                #print(ship.pos, waypoint.pos)
            elif cmd == 'L':
                waypoint.rotate_left(value)
            elif cmd == 'R':
                waypoint.rotate_right(value)
            elif cmd == 'N':
                waypoint.move_in_direction(direction.North(), value)
            elif cmd == 'S':
                waypoint.move_in_direction(direction.South(), value)
            elif cmd == 'E':
                waypoint.move_in_direction(direction.East(), value)
            elif cmd == 'W':
                waypoint.move_in_direction(direction.West(), value)

    print(ship.pos.manhattan_distance(Point2D(0, 0)))


if __name__ == "__main__":
    part1()
    part2()
