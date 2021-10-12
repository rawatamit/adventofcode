class Claim:
    def __init__(self, claim_id, left_edge, top_edge, width, height):
        self.id = claim_id
        self.left_edge = left_edge
        self.top_edge = top_edge
        self.width = width
        self.height = height
    
    def __repr__(self):
        return f'Claim(id={self.id}, {self.left_edge},{self.top_edge}, {self.width},{self.height})'
    
    def __hash__(self):
        return self.id


def parse_claim(s):
    claim_id, info = s.split('@')
    first_part, second_part = info.split(':')
    left_edge, top_edge = first_part.split(',')
    width, height = second_part.split('x')
    return Claim(int(claim_id[1:]),
            int(left_edge), int(top_edge),
            int(width), int(height))


def claim_area(grid, claim):
    y = claim.top_edge
    x = claim.left_edge

    for dx in range(claim.width):
        for dy in range(claim.height):
            yield grid[y+dy][x+dx]


def fill_claim(grid, claim):
    for cell in claim_area(grid, claim):
        cell.add(claim)


def count_claims(grid):
    count = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if len(grid[y][x]) > 1:
                count += 1
    return count


def has_overlap(grid, claim):
    for cell in claim_area(grid, claim):
        if len(cell) != 1:
            return True
    return False


def find_no_overlap(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if len(grid[y][x]) == 1:
                # take this claim from grid as its isolated
                claim = next(iter(grid[y][x]))
                if not has_overlap(grid, claim):
                    return claim.id
    return -1


def draw(grid):
    for row in grid:
        print(''.join(str(x) for x in row))


def main():
    grid = [[set() for _ in range(1000)] for _ in range(1000)]

    with open('d3.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                claim = parse_claim(line)
                fill_claim(grid, claim)
    
    # part 1
    # draw(grid)
    x = count_claims(grid)
    print(x)

    # part 2
    x = find_no_overlap(grid)
    print(x)


main()
