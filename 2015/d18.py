import enum
from aocd import get_data
import copy


class Grid:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.buffer = copy.deepcopy(grid)
        self.rows = len(grid)
        self.cols = len(grid[0])
    
    def __str__(self) -> str:
        return '\n'.join(''.join(row) for row in self.grid)
    def __repr__(self) -> str:
        return str(self)

    def corners(self):
        return ((0, 0), (0, self.cols - 1),
                (self.rows - 1, 0), (self.rows - 1, self.cols - 1))
    
    def turn_on_corners(self):
        for r, c in self.corners():
            self.grid[r][c] = '#'

    def neigbors(self, r, c):
        dr = [-1, -1, -1, +0, +0, +1, +1, +1]
        dc = [-1, +0, +1, -1, +1, -1, +0, +1]
        for i, ri in enumerate(dr):
            nr = r + ri
            nc = c + dc[i]
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                yield nr, nc
    
    def total_on(self):
        return sum(1 for _, row in enumerate(self.grid)
                     for _, cell in enumerate(row)
                     if cell == '#')
    
    def neighbors_on(self, r, c):
        return len([1 for nr, nc in self.neigbors(r, c)
            if self.grid[nr][nc] == '#'])
    
    def next_state(self):
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                # part 2
                if (r, c) in self.corners():
                    self.buffer[r][c] = '#'
                    continue
                on = self.neighbors_on(r, c) 
                if cell == '#':
                    self.buffer[r][c] = '#' if on in (2, 3) else '.'
                else:
                    self.buffer[r][c] = '#' if on == 3 else '.'
        
        self.buffer, self.grid = self.grid, self.buffer


if __name__ == '__main__':
    data = '''
    .#.#.#
    ...##.
    #....#
    ..#...
    #.#..#
    ####..
    '''.strip()
    data = get_data(year=2015, day=18)
    grid = Grid([list(row.strip()) for row in data.splitlines()])
    grid.turn_on_corners() # for part 2
    #print(grid)
    n = 100
    for _ in range(n):
        grid.next_state()
    #print(grid)
    print(grid.total_on())
