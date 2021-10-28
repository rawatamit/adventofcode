def flip(picture):
    return [row[::-1] for row in picture]


def rotate(picture):
    size = len(picture)
    npicture = [[None] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            npicture[i][j] = picture[j][size - i - 1]
    return npicture


def combinations(picture):
    rotations = [rotate(picture)]
    rotations.append(rotate(rotations[-1]))
    rotations.append(rotate(rotations[-1]))

    flips = list(map(flip, rotations))
    return rotations + flips + [picture]


class Pattern:
    def __init__(self, in_pattern, out_pattern) -> None:
        self.in_pattern = in_pattern
        self.out_pattern = out_pattern
    
    def __str__(self) -> str:
        return f'{self.in_pattern} => {self.out_pattern}'
    
    def match(self, picture):
        for comb in combinations(picture):
            if comb == self.in_pattern:
                return self.out_pattern
        return False


def parse_pattern(s):
    inp, outp = s.split('=>')
    return Pattern([[c for c in x] for x in inp.strip().split('/')],
                   [[c for c in x] for x in outp.strip().split('/')])


def get_partition(picture, top_left, bottom_right):
    trow, tcol = top_left
    brow, bcol = bottom_right
    return [[picture[row][col] for col in range(tcol, bcol)]
            for row in range(trow, brow)]


def generate_partitions(picture, partition_size, top_left=(0, 0)):
    size = len(picture)

    # out of bounds?
    if top_left >= (size, size): return

    # calculate dimension for this partition
    trow, tcol = top_left
    brow, bcol = (trow + partition_size, tcol + partition_size)
    bottom_right = (brow, bcol)

    # get the actual partition from the picture
    yield get_partition(picture, top_left, bottom_right)

    # if columns to move, move in the same row towards the end
    if bcol < size:
        ntop_left = (trow, bcol)
        yield from generate_partitions(picture, partition_size, ntop_left)
    # else move down the rows, and start at the first column in row
    elif brow < size:
        ntop_left = (brow, 0)
        yield from generate_partitions(picture, partition_size, ntop_left)


def generate_partitions2(picture, partition_size):
    size = len(picture)

    for row in range(0, size, partition_size):
        for col in range(0, size, partition_size):
            top_left = (row, col)
            bottom_right = (row + partition_size, col + partition_size)
            yield get_partition(picture, top_left, bottom_right)


def fill(picture, pattern, top_left, bottom_right):
    trow, tcol = top_left
    brow, bcol = bottom_right
    for i in range(trow, brow):
        for j in range(tcol, bcol):
            picture[i][j] = pattern[i - trow][j - tcol]


def enhance(picture, rules, npartitions, partition_size):
    npartition_size = partition_size + 1
    nsize = npartition_size * npartitions
    npicture = [[None] * nsize for _ in range(nsize)]

    # markers for the new picture we are building
    trow, tcol = (0, 0)
    brow, bcol = (npartition_size, npartition_size)

    pic_iter = generate_partitions2(picture, partition_size)

    for pic in pic_iter:
        for rule in rules:
            pattern = rule.match(pic)
            if pattern:
                fill(npicture, pattern, (trow, tcol), (brow, bcol))

                # update indices for new picture
                if bcol < nsize:
                    trow, tcol = trow, bcol
                elif brow < nsize:
                    trow, tcol = brow, 0
                brow, bcol = trow + npartition_size, tcol + npartition_size
    
    return npicture


def partition(picture, rules):
    size = len(picture)

    if size % 2 == 0:
        npartitions = size // 2
    else:
        assert size % 3 == 0
        npartitions = size // 3
    
    partition_size = size // npartitions
    return enhance(picture, rules, npartitions, partition_size)


def part1(picture, rules, niter=1):
    for _ in range(niter):
        picture = partition(picture, rules)
    #draw(picture)

    on_pixel = sum(sum(1 for x in row if x == '#') for row in picture)
    print(on_pixel)


def draw(picture):
    for row in picture:
        print(''.join(row))
    print()


def main():
    picture = [['.','#','.'], ['.','.','#'], ['#','#','#']]

    rules = []
    with open('d21.txt') as fin:
        for line in fin:
            line = line.strip()
            if line: rules.append(parse_pattern(line))

    part1(picture, rules, 18)


main()
