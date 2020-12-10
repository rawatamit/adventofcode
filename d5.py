def get_range(c, l, u):
    if c == 'F' or c == 'L':
        return l, (l + u) // 2
    elif c == 'B' or c == 'R':
        return ((l + u) // 2) + 1, u
    else:
        raise Exception('unknown range character {}'.format(c))


def seat_search(boarding_pass):
    lr, ur = 0, 127
    for c in boarding_pass[:-3]:
        lr, ur = get_range(c, lr, ur)
    
    assert lr == ur

    lc, uc = 0, 7
    for c in boarding_pass[-3:]:
        lc, uc = get_range(c, lc, uc)
    
    assert lc == uc
    return lr, lc


def seat_id(row, col):
    return row * 8 + col


def missing_seat(boarding_passes):
    sorted_seats = sorted([seat_search(boarding_pass)
        for boarding_pass in boarding_passes])
    
    for i in range(1, len(sorted_seats) - 1):
        a = sorted_seats[i-1]
        b = sorted_seats[i]
        c = sorted_seats[i+1]
        if (a + 1 != b) or (b + 1 != c):
            print(a, b, c)


if __name__ == '__main__':
    with open('d5.txt') as fin:
        # max_id = -1
        # for line in fin:
        #     if line:
        #         max_id = max([max_id, seat_id(line.strip())])
        # print(max_id)

        boarding_passes = [line.strip() for line in fin]
        print(missing_seat(boarding_passes))
