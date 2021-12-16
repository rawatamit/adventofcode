from aocd.models import Puzzle
import re


def is_nice(s):
    if len(re.findall(r'[aeiou]', s)) > 2 and re.search(r'(\w)\1{1,}', s):
        return not any(re.search(needle, s)
                for needle in (r'ab', r'cd', r'pq', r'xy'))
    
    return False


def is_nice2(s):
    return re.search(r'(\w{2}).*\1', s) and re.search(r'(\w).\1', s)


if __name__ == '__main__':
    puzzle = Puzzle(year=2015, day=5)
    data = puzzle.input_data

    assert is_nice('ugknbfddgicrmopn')
    assert is_nice('aaa')
    assert not is_nice('jchzalrnumimnmhp')
    assert not is_nice('haegwjzuvuyypxyu')
    assert not is_nice('dvszwmarrgswjxmb')

    print(len([s for s in data.split('\n') if is_nice(s)]))

    assert is_nice2('qjhvhtzxzqqjkmpb')
    assert is_nice2('xxyxx')
    assert not is_nice2('uurcxstgmygtbstg')
    assert not is_nice2('ieodomkazucvgmuy')

    print(len([s for s in data.split('\n') if is_nice2(s)]))
