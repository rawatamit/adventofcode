class Grid:
    def __init__(self, stream):
        self.grid = []
        self.row = 0
        self.col = 0
        for line in stream:
            self.grid.append(line.strip())
        self.nrows = len(self.grid)
        self.ncols = len(self.grid[0])
 
    def __str__(self):
        return str(self.grid)
    
    def get_cell(self, row, col):
        row %= self.nrows
        col %= self.ncols
        return self.grid[row][col]
    
    def move_on_grid(self, next_move):
        tree_count = 0
        self.row = 0
        self.col = 0

        while self.row <= self.nrows:
            if self.get_cell(self.row, self.col) == '#':
                tree_count += 1
            self.row, self.col = next_move(self.row, self.col)
        return tree_count
    
    def strategies(self):
        ans = 1
        for dr, dc in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]:
            ans *= self.move_on_grid(lambda r, c: (r + dr, c + dc))
        return ans


if __name__ == '__main__':
    with open('d3.txt') as fin:
        g = Grid(fin)
    print(g.strategies())
