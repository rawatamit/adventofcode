COMPLETE = 1
LOOP = 2


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

    while iptr < len(bcode):
        op, arg = bcode[iptr]

        if iptr in visited:
            return LOOP, acc

        visited.add(iptr)
        if op == 'nop':
            iptr += 1
        elif op == 'acc':
            acc += arg
            iptr += 1
        elif op == 'jmp':
            iptr += arg
    return COMPLETE, acc


def modify_and_run(bcode):
    def run_after_changing(bcode_modified, i, to_op):
        save = bcode_modified[i]
        bcode_modified[i] = (to_op, arg)
        status, acc = execute_bytecode(bcode_modified)
        bcode_modified[i] = save
        return status, acc
    
    bcode_modified = bcode[:]
    for i in range(len(bcode)):
        op, arg = bcode[i]
        for from_op, to_op in [('nop', 'jmp'), ('jmp', 'nop')]:
            if op == from_op:
                status, acc = run_after_changing(bcode_modified, i, to_op)
                if status == COMPLETE:
                    return acc


if __name__ == "__main__":
    with open('d8.txt') as fin:
        bcode = read_bytecode(fin)
    acc = modify_and_run(bcode)
    print(acc)
