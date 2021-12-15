from aocd.models import Puzzle
from heapq import heappop, heappush


class Grid:
    def __init__(self, rows, times=1) -> None:
        self._rows = rows
        self._times = times
        self._init_rows = len(rows)
        self._init_cols = len(rows[0])
        self._nrows = self._init_rows * times
        self._ncols = self._init_cols * times
    
    @property
    def nrows(self):
        return self._nrows

    @property
    def ncols(self):
        return self._ncols
    
    def getcell(self, x, y):
        assert 0 <= x < self.nrows and 0 <= y < self.ncols

        # calculate position inside original grid
        row = x % self._init_rows
        col = y % self._init_cols

        # find which portion of grid we are in, grid extends both ways
        # 'times' times.
        # NOTE: Both x any y portion should be same.
        x_portion = x // self._init_rows
        y_portion = y // self._init_cols

        # every portion increases value by one.
        val = int(self._rows[row][col]) + x_portion + y_portion

        # wrap value to 1 if val > 9
        return val - 9 if val > 9 else val

    def neighbors(self, x, y):
        dxs = [0, 0, -1, +1]
        dys = [1, -1, 0, 0]

        for i, dx in enumerate(dxs):
            nx = x + dx
            ny = y + dys[i]

            if 0 <= nx < self.nrows and 0 <= ny < self.ncols:
                yield nx, ny
    
    def draw(self):
        display = []

        for x in range(self.nrows):
            row = [self.getcell(x, y) for y in range(self.ncols)]
            display.append([str(x) for x in row])
        
        for row in display:
            print(''.join(row))


def dijkstra(grid, start, end):
    Q = [(0, start)]
    D = {start: 0}

    while Q:
        dist_start, u = heappop(Q)
        x, y = u

        if u == end: return dist_start

        for nx, ny in grid.neighbors(x, y):
            v = (nx, ny)
            cur_dist = D.get(v, float('inf'))

            if v not in D and grid.getcell(nx, ny) + D[u] < cur_dist:
                D[v] = grid.getcell(nx, ny) + D[u]
                heappush(Q, (D[v], v))

    return -1


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=15)

    data = '''1163751742
        1381373672
        2136511328
        3694931569
        7463417111
        1319128137
        1359912421
        3125421639
        1293138521
        2311944581'''
    
    data = puzzle.input_data
    rows = [row.strip() for row in data.split('\n')]

    # part 1
    grid = Grid(rows)
    start = (0, 0)
    end = (grid.nrows - 1, grid.ncols - 1)
    print(dijkstra(grid, start, end))

    # part 2
    grid = Grid(rows, times=5)
    start = (0, 0)
    end = (grid.nrows - 1, grid.ncols - 1)
    print(dijkstra(grid, start, end))

    #grid.draw()
