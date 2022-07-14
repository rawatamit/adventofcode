from aocd import get_data
from json import loads
import re


class AuntSue:
    def __init__(self, num) -> None:
        self.num = num
        self.children = None
        self.cats = None
        self.goldfish = None
        self.trees = None
        self.cars = None
        self.perfumes = None
        self.samoyeds = None
        self.pomeranians = None
        self.akitas = None
        self.vizslas = None
    
    def __str__(self) -> str:
        return f'AuntSue({vars(self)})'
    def __repl__(self) -> str:
        return str(self)


if __name__ == '__main__':
    data = get_data(year=2015, day=16)
    ticker_tape = loads('''
    {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1}
    ''')
    pattern = 'Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)'
    aunts = []
    for line in data.splitlines():
        sue_num, prop1, val1, prop2, val2, prop3, val3 = re.findall(pattern, line)[0]
        aunt = AuntSue(int(sue_num))
        setattr(aunt, prop1, int(val1))
        setattr(aunt, prop2, int(val2))
        setattr(aunt, prop3, int(val3))
        aunts.append(aunt)
    
    max_count1 = 0
    from_sue1 = None
    for aunt in aunts:
        count1 = 0
        for prop, val in ticker_tape.items():
            if getattr(aunt, prop) == val:
                count1 += 1
        if count1 > max_count1:
            max_count1 = count1
            from_sue1 = aunt
    print(from_sue1, max_count1)

    prop_fns2 = {'cats': lambda aunt, val: aunt.cats is not None and aunt.cats > val,
                'trees': lambda aunt, val: aunt.trees is not None and aunt.trees > val,
                'pomeranians': lambda aunt, val: aunt.pomeranians is not None and aunt.pomeranians < val,
                'goldfish': lambda aunt, val: aunt.goldfish is not None and aunt.goldfish < val}
    max_count2 = 0
    from_sue2 = None
    for aunt in aunts:
        count2 = 0
        for prop, val in ticker_tape.items():
            if prop in prop_fns2:
                if prop_fns2[prop](aunt, val):
                    count2 += 1
            elif getattr(aunt, prop) == val:
                count2 += 1
        if count2 > max_count2:
            max_count2 = count2
            from_sue2 = aunt
    print(from_sue2, max_count2)
