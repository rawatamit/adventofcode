import string


def reverse_polarity(a, b):
    if (a.islower() and b.isupper()) or (a.isupper() and b.islower()):
        return a.lower() == b.lower()
    return False


def reduce_polymer(polymer, ignore=set()):
    polymer_l = []
    
    for c in polymer:
        if c in ignore: continue
        if polymer_l and reverse_polarity(polymer_l[-1], c):
            polymer_l.pop()
        else:
            polymer_l.append(c)
    
    return ''.join(polymer_l)


def reduce_polymer_old(polymer):
    polymer_l = [c for c in polymer]

    while True:
        reduce_index = -1

        for i in range(len(polymer_l)-1):
            if reverse_polarity(polymer_l[i], polymer_l[i+1]):
                reduce_index = i
                #print(f'will remove {polymer_l[i]} {polymer_l[i+1]}')
                break

        if reduce_index != -1:
            # remove index i
            del polymer_l[reduce_index]
            # remove index i+1
            del polymer_l[reduce_index]
        else:
            # didn't find anything to reduce this iteration
            break
    
    return ''.join(polymer_l)


def part2(polymer):
    l = string.ascii_lowercase
    u = string.ascii_uppercase
    min_len = float('inf')

    for i in range(len(l)):
        rpolymer = reduce_polymer(polymer, ignore={l[i], u[i]})
        min_len = min(min_len, len(rpolymer))
    
    return min_len


def main():
    with open('d5.txt') as fin:
        polymer = fin.read().strip()

    # part 1
    rp = reduce_polymer(polymer)
    print(len(rp))

    # part 2
    #x = part2(polymer)
    x = part2(rp)
    print(x)

main()
