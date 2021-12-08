def dragon_curve(a):
    b = ''.join(['1' if x == '0' else '0' for x in a[::-1]])
    return f'{a}0{b}'


def no_overlap_groups_of(s, n):
    for i in range(0, len(s), n):
        yield s[i:i+n]


def checksum(s):
    chksum = []
    chksum_str = s

    while len(chksum) % 2 == 0:
        chksum = ['1' if gp in ('00', '11') else '0'
                  for gp in no_overlap_groups_of(chksum_str, 2)]

        chksum_str = ''.join(chksum)
    
    return chksum_str


def fill_disk(s, size):
    while len(s) < size:
        s = dragon_curve(s)
    return checksum(s[:size])


if __name__ == '__main__':
    s = '11011110011011101'
    print(fill_disk(s, 272))
    print(fill_disk(s, 35651584))
