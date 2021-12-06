from collections import Counter


def part1(binums):
    gamma_str = []
    epsilon_str = []

    for freq in map(lambda x: Counter(x), zip(*binums)):
        gamma_bit, epsilon_bit = freq.most_common(2)
        gamma_str.append(gamma_bit[0])
        epsilon_str.append(epsilon_bit[0])
    
    gamma = int(''.join(gamma_str), base=2)
    epsilon = int(''.join(epsilon_str), base=2)
    return gamma * epsilon


def find_digits(binums, freq_fn):
    candidates = binums[:]
    cur_index = 0

    while len(candidates) > 1:
        freq_str = [freq_fn(freq.most_common(2))
                    for freq in map(lambda x: Counter(x), zip(*candidates))]

        candidates = [cand for cand in candidates
                           if cand[cur_index] == freq_str[cur_index]]
        cur_index += 1
    
    return int(''.join(candidates[0]), base=2)


def freq_fn(freqs, index, default_digit):
    # index is 0 if most frequent bit is required
    # 1 if least frequent bit is required
    if len(freqs) == 1:
        return freqs[0][0]

    most_common_bit, least_common_bit = freqs
    
    if most_common_bit[1] != least_common_bit[1]:
        return freqs[index][0]
    else:
        return default_digit


def part2(binums):
    o2 = find_digits(binums, lambda freqs: freq_fn(freqs, 0, '1'))
    co2 = find_digits(binums, lambda freqs: freq_fn(freqs, 1, '0'))
    return o2 * co2


if __name__ == '__main__':
    with open('d3.txt') as fin:
        binums = fin.read().split('\n')
    
    print(part1(binums))
    print(part2(binums))
