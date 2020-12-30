import math


def cmd_components(cmd):
    return cmd[0], int(cmd[1:])


def is_directional_cmd(cmd):
    return cmd[0] in ('L', 'R')


class ShipVector:
    def __init__(self):
        self.pos = (0, 0)
    
    @property
    def X(self):
        return self.pos[0]
    
    @property
    def Y(self):
        return self.pos[1]

    def rotate_counter_clockwise(self, degrees):
        # cos(theta) -sin(theta)
        # sin(theta)  cos(theta)
        x = round(self.X * math.cos(math.pi/180 * degrees)
            + (- self.Y * math.sin(math.pi/180 * degrees)))
        y = round(self.X * math.sin(math.pi/180 * degrees)
            + self.Y * math.cos(math.pi/180 * degrees))
        self.pos = (x, y)

    def update_direction(self, cmd):
        direction, degrees = cmd_components(cmd)

        if direction == 'L':
            self.rotate_counter_clockwise(degrees)
        elif direction == 'R':
            self.rotate_counter_clockwise(360 - degrees)

    def update_position(self, cmd):
        direction, value = cmd_components(cmd)
        if direction == 'F':
            direction = self.get_direction()

        if direction == 'E':
            self.pos[0] += value
        elif direction == 'W':
            self.pos[0] += value
        elif direction == 'N':
            self.pos[1] += value
        elif direction == 'S':
            self.pos[1] -= value


def move_ship(stream):
    ship = ShipVector()
    for cmd in stream:
        cmd = cmd.strip()
        if is_directional_cmd(cmd):
            ship.update_direction(cmd)
        else:
            ship.update_position(cmd)
    return ship


if __name__ == "__main__":
    with open('d12.txt') as fin:
        ship = move_ship(fin)
        print(ship.dir, ship.xpos, ship.ypos)
