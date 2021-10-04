from intcode_computer import IntCodeComputerMk2

def block_tiles(output):
    count = 0
    for i in range(2, len(output), 3):
        if output[i] == 2:
            count += 1
    return count

def main():
    with open('d13.txt') as fin:
        program = [int(x) for x in fin.readline().split(',') if x]
    
    ## part 1
    # output = IntCodeComputerMk2(program).execute()
    # print(block_tiles(output))

    ## part 1
    program[0] = 2


main()
