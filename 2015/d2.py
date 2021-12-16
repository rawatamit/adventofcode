from aocd.models import Puzzle


if __name__ == '__main__':
    puzzle = Puzzle(year=2015, day=2)
    data = puzzle.input_data

    total_paper = 0
    total_ribbon = 0

    for line in data.split('\n'):
        a, b, c = sorted([int(x) for x in line.split('x')])
        surface_area = 2 * a * b + 2 * a * c + 2 * b * c
        extra_paper = a * b
        total_paper += surface_area + extra_paper
        # perimeter + volume
        total_ribbon += (2 * a + 2 * b) + (a * b * c)

    print(total_paper, total_ribbon)
