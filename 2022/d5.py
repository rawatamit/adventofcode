from aocd import get_data
import re


def cratemover_9000(crates, moves):
    for n, from_c, to_c in moves:
        from_idx = from_c - 1
        to_idx = to_c - 1

        for _ in range(n):
            disc = crates[from_idx].pop()
            crates[to_idx].append(disc)


def cratemover_9001(crates, moves):
    for n, from_c, to_c in moves:
        from_idx = from_c - 1
        to_idx = to_c - 1

        discs = []
        for _ in range(n):
            disc = crates[from_idx].pop()
            discs.append(disc)
        
        for disc in reversed(discs):
            crates[to_idx].append(disc)


if __name__ == '__main__':
    data = '''    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2'''
    data = get_data(year=2022, day=5)

    reading_crates = True
    crates = None
    moves = []

    for line in data.splitlines():
        if reading_crates:
            if not line:
                reading_crates = False
            else:
                if '1' in line: continue
                if crates is None:
                    crates = [[] for _ in range(len(line) // 3)]
                for disc in re.finditer('\w+', line):
                    if disc.group(0).isdigit():
                        continue
                    crates[disc.start() // 4].append(disc.group(0))
        else:
            moves.append([int(x) for x in re.findall('\d+', line.strip())])
    
    # we want stack semantics for every block, easier to push pop
    for row in crates:
        row.reverse()

    #cratemover_9000(crates, moves)
    cratemover_9001(crates, moves)
    print(''.join(row[-1] for row in crates if row))
