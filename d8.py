def read_bytecode(stream):
    bcode = []
    for line in stream:
        line = line.strip()
        if line:
            op, arg = line.split()
            bcode.append((op, int(arg)))
    return bcode


def execute_bytecode(bcode):
    acc = 0
    iptr = 0
    visited = set()

    while True:
        op, arg = bcode[iptr]

        if iptr in visited:
            print('loop!!!!', iptr, acc)
            break

        visited.add(iptr)
        if op == 'nop':
            iptr += 1
        elif op == 'acc':
            acc += arg
            iptr += 1
        elif op == 'jmp':
            iptr += arg
    

if __name__ == "__main__":
    with open('d8.txt') as fin:
        bcode = read_bytecode(fin)
    execute_bytecode(bcode)
