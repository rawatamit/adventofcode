from aocd.models import Puzzle
import hashlib


def get_start_zeros(s, n=1):
    i = 0
    shash = ''

    while not shash.startswith('0' * n):
        i += 1
        check_str = f'{s}{i}'.encode('utf-8')
        shash = hashlib.md5(check_str).hexdigest()
    
    return i


if __name__ == '__main__':
    puzzle = Puzzle(year=2015, day=4)
    data = puzzle.input_data

    print(get_start_zeros(data, n=5))
    print(get_start_zeros(data, n=6))
