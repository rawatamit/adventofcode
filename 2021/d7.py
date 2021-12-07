from aocd.models import Puzzle
import z3


def z3_abs(x):
    return z3.If(x >= 0, x, -x)


def z3_constraints(positions):
    optimizer = z3.Optimize()
    x = z3.Int('x')

    optimizer.add(x >= min(positions))
    optimizer.add(x <= max(positions))

    total_fuel = z3.Sum([z3_abs(pos - x) for pos in positions])
    optimizer.minimize(total_fuel)
    optimizer.check()
    m = optimizer.model()
    xval = m.eval(x).as_long()
    return xval
    return sum([abs(xval - pos) for pos in positions])


def fuel_to(to_pos, positions):
    return sum([abs(to_pos - pos) for pos in positions])


# sum from [x..y]
def S_n(x, y):
    n = abs(x - y)
    return (n * (n + 1)) >> 1


def fuel_to(to_pos, positions):
    return sum([S_n(to_pos, pos) for pos in positions])


def minimize_fuel(positions):
    min_fuel = float('inf')
    for to_pos in range(min(positions), max(positions) + 1):
        min_fuel = min(min_fuel, fuel_to(to_pos, positions))
    return min_fuel


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=7)
    data = puzzle.input_data

    positions = [int(x) for x in data.split(',')]
    #print(len(positions))

    #print(max(positions))

    #positions = [16,1,2,0,4,2,7,1,2,14]
    print(z3_constraints(positions))
    #print(minimize_fuel(positions))

    #print(sum([abs(1535 - pos) for pos in positions]))
    #print(positions)
