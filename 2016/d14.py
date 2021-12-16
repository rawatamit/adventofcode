import hashlib
import re
import itertools
from aocd.models import Puzzle


class HashGen:
    def __init__(self, s, stretch=0) -> None:
        assert stretch >= 0
        self.hashes = []
        self.s = s
        self.stretch = stretch
    
    def _gen_hash(self, i):
        s = f'{self.s}{i}'.encode('utf-8')
        s = hashlib.md5(s).hexdigest()

        for _ in range(self.stretch):
            s = hashlib.md5(s.encode('utf-8')).hexdigest()
        
        return s
    
    def _fill_hashes(self, i):
        n = len(self.hashes)

        if n <= i:
            # minimum hashes to fill
            delta = i - n

            # fill delta + 999 hashes starting from n
            for j in range(n, n + delta + 1000):
                self.hashes.append(self._gen_hash(j))
    
    def get_hash(self, i):
        self._fill_hashes(i)
        return self.hashes[i]


def check_next_1000(c, i, hgen):
    needle = c * 5

    # check for a 5 length group starting at i
    # with the same characters as three length group
    for j in range(i+1, i+1001):
        nhash = hgen.get_hash(j)
        if re.search(needle, nhash):
            return True
    
    return False


def is_key(shash, i, hgen):
    # find a three length group in the hash
    regex = r'(\w)\1{2}'
    if res := re.search(regex, shash):
        # if there is such a group, check next 1000 entries
        return check_next_1000(res.group(1), i, hgen)
    
    return False


def get_keys(hgen, n=1):
    return itertools.islice(
            filter(lambda i: is_key(hgen.get_hash(i), i, hgen),
                    itertools.count()),
            n)


if __name__ == '__main__':
    puzzle = Puzzle(year=2016, day=14)
    data = puzzle.input_data

    salt = data.strip()
    #salt = 'abc'

    hgen = HashGen(salt)
    keys = list(get_keys(hgen, 64))
    #print(keys)
    print(keys[-1])

    hgen = HashGen(salt, stretch=2016)
    keys = list(get_keys(hgen, 64))
    print(keys[-1])
