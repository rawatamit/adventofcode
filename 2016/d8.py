def nrows(screen):
    return len(screen)


def ncols(screen):
    return len(screen[0])


def rotate(l, n):
    # rotate list l by n
    for _ in range(n % len(l)):
        x = l.pop()
        l.insert(0, x)


def rect(screen, A, B):
    for i in range(B):
        for j in range(A):
            screen[i][j] = '#'


def rotate_column(screen, A, B):
    column = [screen[i][A] for i in range(nrows(screen))]
    rotate(column, B)

    for i in range(nrows(screen)):
        screen[i][A] = column[i]


def rotate_row(screen, A, B):
    row = [screen[A][i] for i in range(ncols(screen))]
    rotate(row, B)

    for i in range(ncols(screen)):
        screen[A][i] = row[i]


def draw(screen, A, B):
    for i in range(B):
        row = [screen[i][j] for j in range(A)]
        print(''.join(row))


def pixels_lit(screen):
    return sum(sum(1 for j in range(ncols(screen))
                        if screen[i][j] == '#')
            for i in range(nrows(screen)))


if __name__ == '__main__':
    screen = [['.' for _ in range(50)] for _ in range(6)]

    i = 0
    with open('d8.txt') as fin:
        for line in fin:
            cmd, args = line.split(' ', 1)
            if cmd == 'rect':
                A, B = [int(x) for x in args.split('x')]
                rect(screen, A, B)
            else:
                assert cmd == 'rotate'
                subcmd, args = args.split(' ', 1)
                A, B = [int(x) for x in args[2:].split('by')]

                if subcmd == 'row':
                    rotate_row(screen, A, B)
                elif subcmd == 'column':
                    rotate_column(screen, A, B)
         
        print(pixels_lit(screen))
        draw(screen, 50, 6)
