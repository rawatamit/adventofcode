from aocd import get_data


def get_strength(cycles, regx, impcycles):
    for cycle in cycles:
        if cycle in impcycles:
            return regx * cycle
    return 0


def screen_loc(cycle):
    # cycle starts with 1
    return ((cycle - 1) // 40, (cycle - 1) % 40)


if __name__ == '__main__':
    data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
    data = get_data(year=2022, day=10)
    cycle = 1
    regx = 1
    total = 0
    cycles = [20, 60, 100, 140, 180, 220]
    insts = data.split('\n')
    for inst in insts:
        if inst.startswith('noop'):
            total += get_strength((cycle,), regx, cycles)
            cycle += 1
        else:
            total += get_strength((cycle, cycle+1), regx, cycles)
            val = int(inst.split()[1])
            cycle += 2
            regx += val

    print('part1', total)

    cycle = 1
    regx = 1
    screen = [['.' for _ in range(40)]
              for _ in range(6)]
    for inst in insts:
        # screen pixels are 0 based. regx starts at 1.
        sprite_pos = [regx-1, regx, regx+1]

        if inst.startswith('noop'):
            rowidx, colidx = screen_loc(cycle)
            if colidx in sprite_pos:
                screen[rowidx][colidx] = '#'
            cycle += 1
        else:
            rowidx, colidx = screen_loc(cycle)
            if colidx in sprite_pos:
                screen[rowidx][colidx] = '#'
            # cycle+1 is also part of this instruction.
            rowidx2, colidx2 = screen_loc(cycle + 1)
            if colidx2 in sprite_pos:
                screen[rowidx2][colidx2] = '#'

            val = int(inst.split()[1])
            cycle += 2
            regx += val

    print('\n'.join(''.join(row) for row in screen))

