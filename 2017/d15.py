def generator(mul_factor, prev_value, multiple_of=1):
    mul_factor = mul_factor
    prev_value = prev_value
    div_factor = 2147483647
    multiple_of = multiple_of
    
    def next():
        nonlocal prev_value, mul_factor, div_factor, multiple_of

        done = False
        while not done:
            next_value = (prev_value * mul_factor) % div_factor
            prev_value = next_value
            if (next_value % multiple_of) == 0:
                done = True
        return next_value
    
    return next


def solve(genA, genB, iter):
    count = 0
    last_16_bits = lambda x: x & 0xffff

    for _ in range(iter):
        cA = last_16_bits(genA())
        cB = last_16_bits(genB())
        if cA == cB:
            count += 1
    
    return count


def part1(prevA, prevB):
    gA = generator(16807, prevA)
    gB = generator(48271, prevB)
    return solve(gA, gB, 40000000)


def part2(prevA, prevB):
    gA = generator(16807, prevA, 4)
    gB = generator(48271, prevB, 8)
    return solve(gA, gB, 5000000)


def main():
    ## example
    # prevA = 65
    # prevB = 8921

    # part 1
    prevA = 618
    prevB = 814
    x = part1(prevA, prevB)
    print(x)

    # part 2
    prevA = 618
    prevB = 814
    x = part2(prevA, prevB)
    print(x)

main()
