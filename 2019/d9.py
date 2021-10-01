from intcode_computer import IntCodeComputer

if __name__ == '__main__':
    with open('d9.txt') as fin:
        program = [int(x) for x in fin.readline().split(',') if x]
    
    # print(program)
    IntCodeComputer(program).execute()
