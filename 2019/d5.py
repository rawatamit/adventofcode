from intcode_computer import IntCodeComputerMk1

if __name__ == '__main__':
    with open('d5.txt') as fin:
        program = [int(x) for x in fin.readline().split(',') if x]
    
    # part 1
    x = IntCodeComputerMk1(program, iter([1])).execute()
    print(x)

    # part 2
    x = IntCodeComputerMk1(program, iter([5])).execute()
    print(x)
