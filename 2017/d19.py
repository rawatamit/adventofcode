class Cell:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f'Cell({self.x}, {self.y})'
    
    def __eq__(self, o: object) -> bool:
        if o is None or not isinstance(o, Cell): return False
        return (self.x, self.y) == (o.x, o.y)
    
    def __hash__(self) -> int:
        return hash(self.x * 11 + self.y * 7)


def add_cell(a, b):
    return Cell(a.x + b.x, a.y + b.y)


def neighbor(cell, dir):
    dirmap = {'U': Cell(0, +1), 'D': Cell(0, -1),
              'L': Cell(-1, 0), 'R': Cell(+1, 0)}
    
    return add_cell(cell, dirmap[dir])


def isvalid(cell, G):
    rows = len(G)
    cols = len(G[0])
    return 0 <= cell.x < cols and 0 <= cell.y < rows


def getcell(cell, G):
    return G[cell.y][cell.x]


def reverse_dir(dir):
    return {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}[dir]


def change_dir(cell, G, curdir):
    for dir in ('U', 'D', 'L', 'R'):
        if reverse_dir(dir) != curdir:
            ncell = neighbor(cell, dir) 
            if isvalid(ncell, G) and getcell(ncell, G) != ' ':
                return dir


def next_cell(cell, curdir, G, path):
    content = getcell(cell, G)

    if content == '+':
        return change_dir(cell, G, curdir)
    elif content.isalpha():
        path.append(content)
        return curdir
    elif content != ' ':
        return curdir


def explore(G):
    cell = Cell(G[0].index('|'), 0)
    # start moving down
    curdir = 'U'
    path = []
    steps = 0
    
    while True:
        cell = neighbor(cell, curdir)
        steps += 1

        curdir = next_cell(cell, curdir, G, path)
        if curdir is None: break
    
    return path, steps


def main():
    G = []
    with open('d19.txt') as fin:
        for line in fin:
            if line.strip():
                # only remove \n character, don't strip!!
                G.append(line[:-1])
    
    path, steps = explore(G)
    print(''.join(path), steps)


main()
