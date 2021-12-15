from aocd.models import Puzzle
from collections import defaultdict


def groups_of(s, n):
    i = 0
    while i+n <= len(s):
        yield s[i:i+n]
        i += 1


def transform_polymer(template, rules, times=1):
    prev_template = list(template)

    for _ in range(times):
        transformed = []
        for gp in groups_of(prev_template, 2):
            pair = ''.join(gp)
            rule = rules.get(pair, None)
            if rule is not None:
                transformed.extend((pair[0], rule))
        
        transformed.append(template[-1])
        prev_template = transformed
    
    return ''.join(transformed)


def transform_polymer2(template, rules, times=1):
    pair_count = defaultdict(int)

    for gp in groups_of(template, 2):
        pair_count[gp] += 1
    
    # keep track of frequencies for pairs
    for _ in range(times):
        new_pair_count = defaultdict(int)

        for pair, count in pair_count.items():
            transform = rules.get(pair, None)

            assert transform is not None

            pair1 = pair[0] + transform
            pair2 = transform + pair[1]

            new_pair_count[pair1] += count
            new_pair_count[pair2] += count
        
        pair_count = new_pair_count

    freqs = defaultdict(int)
    for pair, count in pair_count.items():
        freqs[pair[0]] += count
    
    # last character in template isn't counted above
    freqs[template[-1]] += 1
    
    sorted_freq = sorted(freqs.values())
    return sorted_freq[-1] - sorted_freq[0]


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=14)

    data = '''NNCB

        CH -> B
        HH -> N
        CB -> H
        NH -> C
        HB -> C
        HC -> B
        HN -> C
        NN -> C
        BH -> H
        NC -> B
        NB -> B
        BN -> B
        BB -> N
        BC -> B
        CC -> N
        CN -> C'''

    data = puzzle.input_data
    rules = {}

    for line in data.split('\n'):
        line = line.strip()

        if line and '->' in line:
            pair, element = line.split(' -> ')
            rules[pair] = element
        elif line:
            polymer_template = line

    print(transform_polymer2(polymer_template, rules, times=10))
    print(transform_polymer2(polymer_template, rules, times=40))
