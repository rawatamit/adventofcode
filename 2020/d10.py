def generate_comb_all(adapters, used, connection, i):
    current = 0 if i == 0 else connection[i - 1]
    next_possible = [adapter for adapter in adapters
                     if adapter - current in (1, 2, 3)
                     and not used[adapter]]

    if next_possible:
        for option in next_possible:
            used[option] = True
            yield from generate_comb_all(adapters, used, connection + [option], i + 1)
            used[option] = False
    else:
        yield connection


def num_total_combinations(adapters, used, connection, i, cache):
    current = 0 if i == 0 else connection[i - 1]
    if current in cache: return cache[current]

    next_possible = [adapter for adapter in adapters
                     if adapter - current in (1, 2, 3)
                     and not used[adapter]]

    if next_possible:
        total = 0
        for option in next_possible:
            used[option] = True
            total += num_total_combinations(adapters, used,
                            connection + [option], i + 1, cache)
            used[option] = False
    else:
        return 1
    
    cache[current] = total
    return cache[current]


def part1(adapters):
    longest_chain = sorted(adapters)
    chain = [0] + longest_chain + [longest_chain[-1] + 3]
    diffs = [chain[i] - chain[i-1] for i in range(1, len(chain))]
    num_3 = len(list(filter(lambda x: x == 3, diffs)))
    num_1 = len(list(filter(lambda x: x == 1, diffs)))
    return num_1 * num_3


def part2(adapters):
    used = {adapter: False for adapter in adapters}
    cache = {}
    return num_total_combinations(adapters, used, [], 0, cache)


if __name__ == '__main__':
    with open('d10.txt') as fin:
        adapters = [int(x) for x in fin.read().split()]
    
    print(part1(adapters))
    print(part2(adapters))
