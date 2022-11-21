from aocd import get_data
from heapq import heappop, heappush


class Grid:
    def __init__(self, depth, nrows, ncols, increment=0) -> None:
        self.depth = depth
        self.ncols = ncols + increment
        self.nrows = nrows + increment
        self.target_x = ncols
        self.target_y = nrows
        self.erosion_levels = [[-1] * (self.ncols + 1)
                               for _ in range(self.nrows + 1)]
        self.grid = [[-1] * (self.ncols + 1)
                     for _ in range(self.nrows + 1)]
        self._build_grid()
    
    def _build_grid(self):
        for y in range(self.nrows + 1):
            for x in range(self.ncols + 1):
                self.get_geologic_index(x, y)
                geologic_index = self.get_geologic_index(x, y)
                cell_erosion_level = (geologic_index + self.depth) % 20183
                cell = None
                if cell_erosion_level % 3 == 0:
                    cell = 0 # rocky
                elif cell_erosion_level % 3 == 1:
                    cell = 1 # wet
                else:
                    cell = 2 # narrow
                self.erosion_levels[y][x] = cell_erosion_level
                self.grid[y][x] = cell

    def get_geologic_index(self, x, y):
        index = -1
        if x == 0 and y == 0:
            index = 0
        elif x == self.target_x and y == self.target_y:
            index = 0
        elif y == 0:
            index = x * 16807
        elif x == 0:
            index = y * 48271
        else:
            index = (self.erosion_levels[y][x - 1] *
                     self.erosion_levels[y - 1][x])
        return index

    def get_cell(self, x, y):
        assert self.nrows > y and len(self.grid[y]) > x
        return self.grid[y][x]

    def draw_grid(self, maxrows, maxcols):
        assert 0 <= maxrows <= self.nrows and 0 <= maxcols <= self.ncols
        for y in range(maxrows + 1):
            for x in range(maxcols + 1):
                cell = self.get_cell(x, y)
                if cell == 0: # rock
                    print('.', end='')
                elif cell == 1: # wet
                    print('=', end='')
                else: # narrow
                    assert(cell == 2)
                    print('|', end='')
            print()


def risk_level(grid, target_y, target_x):
    total_risk = 0
    for y in range(target_y + 1):
        for x in range(target_x + 1):
            total_risk += grid.get_cell(x, y)
    return total_risk


def gear_changes(grid, x, y):
    cell = grid.get_cell(x, y)
    changes = {0: [0, 1],
               1: [0, 2],
               2: [1, 2]}
    return changes[cell]


def explore_cave(grid, target_y, target_x):
    # save: time from start
    # Grid starts at (0,0) which is top.
    neigbors = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
    # state: position, tool
    # climbing gear = 0, torch = 1, neither = 2
    start_state = (0, 0, 1)
    qu = []
    heappush(qu, (0, start_state))
    dist = {start_state: 0}

    while qu:
        cur_dist, cur_state = heappop(qu)
        x, y, cur_tool = cur_state
        if cur_state == (target_x, target_y, 1):
            return cur_dist
        
        if x > 3 * target_x or y > 3 * target_y:
            continue
    
        next_states = []
        # can only move to adjacent nodes with right set of tools
        for dx, dy in neigbors:
            nx = x + dx
            ny = y + dy
            if 0 <= nx and 0 <= ny:
                next_tools = gear_changes(grid, nx, ny)
                if cur_tool in next_tools:
                    next_states.append(((nx, ny, cur_tool), cur_dist + 1))

        # in current cell, we can switch tools that are applicable
        cur_allowed_tools = gear_changes(grid, x, y)
        for switch_tool in range(3):
            if switch_tool in cur_allowed_tools and switch_tool != cur_tool:
                next_states.append(((x, y, switch_tool), cur_dist + 7))
        
        for next_state, ntime in next_states:
            # either climbing gear or torch must be different from previous
            # otherwise the following check will rule them out.
            if ntime < dist.get(next_state, float('inf')):
                dist[next_state] = ntime
                heappush(qu, (ntime, next_state))
    
    return -1


if __name__ == '__main__':
    data = 'depth: 510\ntarget: 10,10'
    data = get_data(year=2018, day=22)
    depth, target = data.splitlines()
    depth = int(depth.split(': ')[1])
    target_x, target_y = [int(n) for n in target.split(': ')[1].split(',')]

    increment = 200
    grid = Grid(depth, target_y, target_x, increment)
    #grid.draw_grid(target_y + 6, target_x + 6)
    # part 1
    print(risk_level(grid, target_y, target_x))

    # part 2
    print(explore_cave(grid, target_y, target_x))
