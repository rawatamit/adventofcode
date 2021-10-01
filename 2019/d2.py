def execute(program):
    ip = 0

    while ip < len(program):
        op = program[ip]

        if op == 1:
            arg1 = program[program[ip + 1]]
            arg2 = program[program[ip + 2]]
            program[program[ip + 3]] = arg1 + arg2
            ip += 4
        elif op == 2:
            arg1 = program[program[ip + 1]]
            arg2 = program[program[ip + 2]]
            program[program[ip + 3]] = arg1 * arg2
            ip += 4
        elif op == 99:
            break
        else:
            raise Exception('unknown opcode: {}'.format(op))
    
    return program[0]


if __name__ == '__main__':
    with open('d2.txt') as fin:
        orig_program = [int(x) for x in fin.readline().split(',')]

    for noun in range(100):
        for verb in range(100):
            program = orig_program[:]
            program[1] = noun
            program[2] = verb
            ans = execute(program)
            if ans == 19690720:
                print(100*noun+verb)
