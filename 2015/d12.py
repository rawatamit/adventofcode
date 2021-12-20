from aocd.models import Puzzle
import re
import json


def find_sum(obj):
    Q = [obj]
    tsum = 0

    while Q:
        obj = Q.pop()

        if isinstance(obj, dict):
            # skip this object if red is a value
            if 'red' not in obj.values():
                Q.extend(obj.values())
        elif isinstance(obj, list):
            Q.extend(obj)
        elif isinstance(obj, int):
            tsum += obj
    
    return tsum


if __name__ == '__main__':
    puzzle = Puzzle(year=2015, day=12)

    data = '{"d":"red","e":[1,2,3,4],"f":5}'
    data = '[1,{"c":"red","b":2},3]'
    data = '[1,"red",5]'

    data = puzzle.input_data

    # part 1
    nums = re.findall('-?\d+', data)
    print(sum(map(int, nums)))

    # part 2
    obj = json.loads(data)
    print(find_sum(obj))
