from aocd import get_data
import collections
import heapq


def get_molecules(compound):
    molecules = []
    i = 0
    while i < len(compound) - 1:
        a = compound[i]
        b = compound[i+1]
        if b.islower():
            molecules.append(''.join((a, b)))
            i += 2
        else:
            molecules.append(a)
            i += 1

    if compound[-1].isupper():
        molecules.append(compound[-1])
    return molecules


def gen(memo, molecules, i, replacements, j, res, nreplace=1):
    if (i, j) in memo:
        return
    memo.add((i, j))

    # out of replacements
    if j >= len(replacements) or nreplace == 0:
        res.add(''.join(molecules))
        return

    # out of molecules
    if i >= len(molecules):
        return

    # try all replacements
    for k in range(j, len(replacements)):
        # this replacement can be made
        a, b = replacements[k]
        if a == molecules[i]:
            save = molecules[i]
            molecules[i] = b
            gen(memo, molecules, i+1, replacements, k+1, res, nreplace-1)
            molecules[i] = save

        # don't replace or a != molecules[i]
        gen(memo, molecules, i+1, replacements, k, res, nreplace)


def similarity(compound, molecule):
    score = 0
    for a, b in zip(compound, molecule):
        if a == b:
            score += 1
    return score


def A_star_fn(compound, molecule):
    return len(molecule)
    return len(compound) - similarity(compound, molecule)


def gen2(compound, start, replacements):
    # e -> start is one step.
    qu = [(A_star_fn(compound, start), 1, start)]
    dist = {start: 1}
    inf = 1<<32

    while qu:
        simscore, steps, node = heapq.heappop(qu)
        #print(node, simscore)
        if node == compound:
            print('ret', node, steps)
            return steps

        molecules = get_molecules(node)
        #print(f'node {node} {molecules}')
        for i, atom in enumerate(molecules):
            for repl in replacements.get(atom, []):
                new_molecule = ''.join(molecules[:i]) + repl + ''.join(molecules[i+1:])
                to_dist = dist.get(new_molecule, inf)
                new_simscore = A_star_fn(compound, new_molecule)

                if len(new_molecule) <= len(compound) and to_dist == inf:
                #if len(new_molecule) <= len(compound) and new_simscore <= simscore:
                    #print(f'from {node}: add {atom} -> {repl} = {new_molecule} {steps+1}')
                    heapq.heappush(qu, (new_simscore, steps+1, new_molecule))
                    dist[new_molecule] = steps+1

    return -1


if __name__ == '__main__':
    example1 = """H => HO
H => OH
O => HH

HOH"""

    example2 = """e => H
e => O
H => HO
H => OH
O => HH

HOH"""

    example3 = """e => H
e => O
H => HO
H => OH
O => HH

HOHOHO"""

    data = example3
    data = get_data(year=2015, day=19)

    replacements = []
    electrons = []
    compound = None
    for line in data.split('\n'):
        line = line.strip()
        if line:
            if '=>' in line:
                lhs, rhs = [x.strip() for x in line.split('=>')]
                if lhs == 'e':
                    electrons.append((lhs, rhs))
                else:
                    replacements.append((lhs, rhs))
            else:
                compound = line

    molecules = get_molecules(compound)
    memo = set()
    res = set()
    gen(memo, molecules, 0, replacements, 0, res)
    print('part1', len(res))

    if False:
        replacement_map = collections.defaultdict(list)
        for a, b in replacements:
            replacement_map[a].append(b)

        all_steps = []
        for _, start in electrons:
            print('electron', start)
            steps = gen2(compound, start, replacement_map)
            if steps > 0:
                all_steps.append(steps)
        print('part2', sorted(all_steps)[0])

