from collections import defaultdict


def is_true(regs, if_cond):
    op_fn = {'>': lambda x, y: x > y,
             '<': lambda x, y: x < y,
             '>=': lambda x, y: x >= y,
             '<=': lambda x, y: x <= y,
             '==': lambda x, y: x == y,
             '!=': lambda x, y: x != y}

    x = regs[if_cond['reg']]
    y = if_cond['value']
    return op_fn[if_cond['op']](x, y)


def perform_operation(regs, operation):
    if operation['op'] == 'inc':
        regs[operation['reg']] += operation['value']
    elif operation['op'] == 'dec':
        regs[operation['reg']] -= operation['value']
    return regs[operation['reg']]


def run_instructions(insts):
    regs = defaultdict(int)
    max_value_ever = -1
    for operation, if_cond in insts:
        if is_true(regs, if_cond):
            reg_value = perform_operation(regs, operation)
            max_value_ever = max(max_value_ever, reg_value)

    return regs, max_value_ever


def parse_instruction(s):
    operation, if_cond = s.split('if')
    oplist = operation.split()
    if_list = if_cond.split()
    return ({'op': oplist[1].strip(),
            'reg': oplist[0].strip(),
            'value': int(oplist[2])},
           {'op': if_list[1].strip(),
            'reg': if_list[0].strip(),
            'value': int(if_list[2])})


def main():
    insts = []
    with open('d8.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                insts.append(parse_instruction(line))
    
    regs, max_value_ever = run_instructions(insts)

    # part 1
    print(max(regs.values()))

    # part 2
    print(max_value_ever)

main()
