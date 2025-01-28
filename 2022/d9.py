from aocd import get_data


def all_neighbors(r, c):
    dr = [-1, 0, 0, 1, -1, -1, 1, 1]
    dc = [0, -1, 1, 0, -1, 1, -1, 1]
    neighbors = {(r + dr[i], c + dc[i]): (dr[i], dc[i])
                    for i in range(len(dr))}
    return neighbors


def move_tail(head, tail):
    # tail is not touching head. Assume at most two step separation.
    if abs(head[0] - tail[0]) > 1 or abs(head[1] - tail[1]) > 1:
        diagn2 = all_neighbors(*head)
        for ntail, _ in all_neighbors(*tail).items():
            dr, dc = diagn2.get(ntail, (None, None))
            if dr is not None:
                # subtract direction to get closer to head
                return (tail[0]-dr, tail[1]-dc)

    # tail is touching head
    return tail


def solve(moves, numtails=1):
    head = (0, 0)
    tails = [(0, 0) for _ in range(numtails)]
    all_visited = set()

    for dir, dist in moves:
        for _ in range(dist):
            if dir == 'D':
                head = (head[0]+1, head[1])
            elif dir == 'U':
                head = (head[0]-1, head[1])
            elif dir == 'L':
                head = (head[0], head[1]-1)
            elif dir == 'R':
                head = (head[0], head[1]+1)

            phead = head
            for i in range(len(tails)):
                tails[i] = move_tail(phead, tails[i])
                phead = tails[i]
            all_visited.add(tails[-1])

    return len(all_visited)


if __name__ == '__main__':
    example1 = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

    example2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

    data = example1
    data = get_data(year=2022, day=9)

    moves = []
    for line in data.split('\n'):
        dir, dist = line.strip().split()
        moves.append((dir, int(dist)))

    print('part1', solve(moves))
    print('part2', solve(moves, numtails=9))

