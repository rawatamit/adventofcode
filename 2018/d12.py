from aocd import get_data


def get_pattern(state, index):
    patt = [('#' if i + index in state else '.')
            for i in [-2, -1, 0, 1, 2]]
    return ''.join(patt)


def next_state(state, combs):
    next_state = set()
    start = min(state)
    end = max(state)
    for i in range(start - 3, end + 4):
        patt = get_pattern(state, i)
        if combs.get(patt, '.') == '#':
            next_state.add(i)
    return next_state


if __name__ == '__main__':
    data = '''initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #'''

    data = get_data(year=2018, day=12)
    lines = data.splitlines()
    # only save indices for pots
    init_state = {i for i, c in enumerate(lines[0].split(': ')[1])
                    if c == '#'}
    combs = {}
    for line in lines[2:]:
        state, val = line.split(' => ')
        combs[state] = val

    state = init_state
    times = 20
    # part 1
    #for _ in range(times):
    #    state = next_state(state, combs)
    #print(sum(state))

    ngen = 0
    last_sum = 0
    # In this input, after generation 161, all the other
    # generations add 73 to the sum. To find the total sum
    # we can find the sum of first 161 generations, and then
    # we can sum 73 upto 50000000000.
    for _ in range(200):#50000000000):
        #state = next_state(state, combs)
        ngen += 1
        s = sum(state)
        #print(ngen, s, s - last_sum)
        last_sum = s
    
    last_sum = 0
    total_sum = 0
    # sum first 200 generations, after that 73 repeats
    for _ in range(200):
        state = next_state(state, combs)
        cur_sum = sum(state)
        total_sum += cur_sum - last_sum
        last_sum = cur_sum
    
    total_sum += (50000000000 - 200) * 73
    print(total_sum)
