import asyncio
from intcode_computer import IntCodeComputerMk2

class HullRobot:
    def __init__(self, start_panel_color=0):
        self.x = 0
        self.y = 0
        self.dir = 'U'
        self.angle_cache = {
            'U': {0: 'L', 1: 'R'},
            'D': {0: 'R', 1: 'L'},
            'L': {0: 'D', 1: 'U'},
            'R': {0: 'U', 1: 'D'}}
        self.move_cache = {
            'U': lambda z: (z[0],     z[1] + 1),
            'D': lambda z: (z[0],     z[1] - 1),
            'L': lambda z: (z[0] - 1, z[1]),
            'R': lambda z: (z[0] + 1, z[1]),
        }
        self.grid = {(self.x, self.y): start_panel_color}
    
    def turn_by_angle(self, angle):
        self.dir = self.angle_cache[self.dir][angle]
    
    def paint_panel(self, color):
        self.grid[(self.x, self.y)] = color
    
    def move(self):
        self.x, self.y = self.move_cache[self.dir]((self.x, self.y))
    
    def panel_color(self):
        if (self.x, self.y) not in self.grid:
            self.grid[(self.x, self.y)] = 0
        return self.grid[(self.x, self.y)]
    
    def get_grid_size(self):
        return len(self.grid)
    
    def __str__(self):
        inf = float('inf')
        min_x, max_x = inf, -inf
        min_y, max_y = inf, -inf 
        for (x, y), _ in self.grid.items():
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        
        range_x = abs(abs(max_x) - abs(min_x))
        range_y = abs(abs(max_y) - abs(min_y))

        G = [[' ' for _ in range(range_y+1)] for _ in range(range_x+1)]
        for (x, y), color in self.grid.items():
            x += abs(min_x)
            y += abs(min_y)
            if color == 0:
                G[x][y] = ' '
            else:
                G[x][y] = '#'

        l = []
        for row in G:
            l.append(''.join(row))
        return '\n'.join(l)

class HullRobotComputer:
    def __init__(self, program):
        self.robot = HullRobot(1)
        self.input = asyncio.Queue()
        self.output = asyncio.Queue()
        self.computer = IntCodeComputerMk2(program[:], self.input, self.output)
    
    async def robot_work(self):
        while True:
            color = await self.output.get()
            if color == -1: break
            angle = await self.output.get()
            self.robot.paint_panel(color)
            self.robot.turn_by_angle(angle)
            self.robot.move()
            panel_color = self.robot.panel_color()
            await self.input.put(panel_color)

    async def run_robot(self):
        start_panel_color = self.robot.panel_color()
        await self.input.put(start_panel_color)
        await asyncio.gather(self.computer.execute(), self.robot_work())
    
    def panels_painted(self):
        return self.robot.get_grid_size()

async def main():
    with open('d11.txt') as fin:
        program = [int(x) for x in fin.readline().split(',') if x.strip()]
    
    rc = HullRobotComputer(program)
    await asyncio.gather(rc.run_robot())
    print(rc.panels_painted())

asyncio.run(main())
