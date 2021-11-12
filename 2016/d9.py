from io import StringIO


def run_length(s, repeat):
    num, times = [int(x) for x in repeat.split('x')]
    chars = s.read(num)
    return chars * times


def decompress(s):
    while True:
        c = s.read(1)
        if c == '(':
            repeat = []
            while c != ')':
                repeat.append(c)
                c = s.read(1)
            yield from run_length(s, ''.join(repeat[1:]))
        elif c != '':
            yield c
        else: break


def decompress_complete(s, start, end):
    if start >= end:
        return 0
    elif s[start] == '(':
        # get (num x times)
        index_rbrack = s.index(')', start)

        # start after ')'
        next_start = index_rbrack + 1

        # only want num x times, leave out brackets
        repeat = s[start+1:index_rbrack]

        num, times = [int(x) for x in repeat.split('x')]

        # find the run nested inside this run
        # this run will be generated "times" times
        subrun = times * decompress_complete(s, next_start, next_start + num)

        # next run will be added to the current run
        return subrun + decompress_complete(s, next_start + num, end)
    else:
        # character
        return 1 + decompress_complete(s, start + 1, end)


if __name__ == '__main__':
    with open('d9.txt') as fin:
        compressed_data = fin.read().strip()
        #compressed_data = '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'
        #compressed_data = '(27x12)(20x12)(13x14)(7x10)(1x12)A'
        #compressed_data.replace('\n', '')
        #decoded = list(decompress(StringIO(compressed_data)))
        #s = ''.join(decoded)
        #s = decompress_complete(StringIO(compressed_data))
        s = decompress_complete(compressed_data, 0, len(compressed_data))
        print(s)
