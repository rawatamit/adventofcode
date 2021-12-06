from types import SimpleNamespace
from aocd import get_data


def simulation(state, ticks=1):
    bin = [0 for _ in range(9)]

    for fish in state:
        bin[fish] += 1
    
    # fish 0 becomes fish 6
    # number of 0 fish become 8
    for _ in range(ticks):
        orig_0 = bin[0]

        for i in range(1, len(bin)):
            bin[i-1] = bin[i]

        bin[6] += orig_0
        bin[8] = orig_0
    
    return sum(bin)


if __name__ == '__main__':
    data = get_data(day=6, year=2021)
    state = [int(x) for x in data.split(',')]
    print(simulation(state, 256))
