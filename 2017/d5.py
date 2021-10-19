def num_jumps(offsets, fn=None):
    pc = 0
    njumps = 0

    while pc < len(offsets):
        next_pc = pc + offsets[pc]
        offsets[pc] += fn(offsets[pc])
        njumps += 1
        pc = next_pc
    return njumps


def main():
    with open('d5.txt') as fin:
        offsets = [int(x) for x in fin.read().strip().split()]

    # part 1
    print(num_jumps(offsets[:], fn=lambda _: 1))

    # part 2
    print(num_jumps(offsets[:], fn=lambda offset: -1 if offset >= 3 else 1))

main()
