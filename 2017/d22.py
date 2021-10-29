class Robot:
    def __init__(self, i, j) -> None:
        self.pos = (i, j)
        self.dir = 'U'

        self.dirmap = {
            'U': {'L': 'L', 'R': 'R', 'FORWARD': 'U', 'REVERSE': 'D'},
            'L': {'L': 'D', 'R': 'U', 'FORWARD': 'L', 'REVERSE': 'R'},
            'R': {'L': 'U', 'R': 'D', 'FORWARD': 'R', 'REVERSE': 'L'},
            'D': {'L': 'R', 'R': 'L', 'FORWARD': 'D', 'REVERSE': 'U'}}
        
        self.movemap = {
            'U': lambda x, y: (x - 1, y),
            'D': lambda x, y: (x + 1, y),
            'L': lambda x, y: (x, y - 1),
            'R': lambda x, y: (x, y + 1)}
    
    def change_dir(self, dir):
        self.dir = self.dirmap[self.dir][dir]
    
    def move(self):
        self.pos = self.movemap[self.dir](*self.pos)


class Grid:
    CLEAN = '.'
    INFECTED = '#'
    WEAKENED = 'W'
    FLAGGED = 'F'

    def __init__(self) -> None:
        self.G = {}

    def getnode(self, pos):
        if pos not in self.G:
            self.G[pos] = Grid.CLEAN
        return self.G[pos]

    def setnode(self, pos, value):
        self.G[pos] = value

    def _new_direction(self, curnode, robot):
        return 'R' if curnode == Grid.INFECTED else 'L'
    
    def _new_node_value(self, curnode):
        return Grid.CLEAN if curnode == Grid.INFECTED else Grid.INFECTED
    
    def _is_infected(self, curnode):
        return curnode == Grid.CLEAN

    def _burst(self, robot):
        curnode = self.getnode(robot.pos)

        # change direction
        ndir = self._new_direction(curnode, robot)
        robot.change_dir(ndir)
        
        # change node value
        nval = self._new_node_value(curnode)
        self.setnode(robot.pos, nval)

        # did the robot infect this cell? check is on curnode and not nval
        # as we want to know the state prior to robot's movement not after
        infected = 1 if self._is_infected(curnode) else 0

        # move forward
        robot.move()
        return infected

    def burst(self, robot, n=1):
        return sum(self._burst(robot) for _ in range(n))

    def draw(self):
        max_x = max(x for x,_ in self.G.keys())
        max_y = max(y for _,y in self.G.keys())
        min_x = min(x for x,_ in self.G.keys())
        min_y = min(y for _,y in self.G.keys())

        min_x, min_y = abs(min_x), abs(min_y)

        grid = [[Grid.CLEAN for _ in range(max_y+min_y+1)]
                for _ in range(max_x+min_x+1)]

        for (x, y), v in self.G.items():
            grid[min_x+x][min_y+y] = v
        
        for row in grid:
            print(''.join(row))


class Grid2(Grid):
    def __init__(self) -> None:
        super().__init__()

    def _is_infected(self, curnode):
        return curnode == Grid.WEAKENED

    def _new_direction(self, curnode, robot):
        ndir_map = {Grid.CLEAN: 'L',
                    Grid.WEAKENED: 'FORWARD',
                    Grid.INFECTED: 'R',
                    Grid.FLAGGED: 'REVERSE'}
        
        return ndir_map[curnode]
    
    def _new_node_value(self, curnode):
        nval_map = {Grid.CLEAN: Grid.WEAKENED,
                    Grid.WEAKENED: Grid.INFECTED,
                    Grid.INFECTED: Grid.FLAGGED,
                    Grid.FLAGGED: Grid.CLEAN}
        
        return nval_map[curnode]


def part12(grid_class=Grid, filepath=None, nburst=10, draw=False):
    grid = grid_class()
    nrow = 0
    ncol = 0
    
    with open(filepath) as fin:
        for line in fin:
            line = line.strip()
            if line:
                ncol = len(line)
                for col, c in enumerate(line):
                    grid.setnode((nrow, col), c)
            nrow += 1
    
    robot = Robot(nrow//2, ncol//2)
    total_infected = grid.burst(robot, nburst)

    if draw: grid.draw()

    print(f'robot pos={robot.pos}, dir={robot.dir}')
    print(f'total infected: {total_infected}')


def main():
    part12(Grid, 'd22.txt', 10000)

    part12(Grid2, 'd22.txt', 10000000, draw=False)


main()
