from aocd.models import Puzzle


def get_connect(name):
    if name[0].isdigit():
        return int(name)
    return name


def read_wire(s):
    ops = ['NOT', 'AND', 'OR', 'LSHIFT', 'RSHIFT']
    is_op = any(op for op in ops if op in s)
    
    if not is_op:
        # this is a number or a variable
        # if this is a variable, make a no op instruction
        # so we don't have to handle it separately
        return int(s) if s[0].isdigit() else ('LShift', s, 0)
    elif s.startswith('NOT'):
        _, wname = s.split()
        return ('Not', get_connect(wname))
    else:
        a, op, b = s.split()
        if op == 'AND':
            return ('And', get_connect(a), get_connect(b))
        elif op == 'OR':
            return ('Or', get_connect(a), get_connect(b))
        elif op == 'LSHIFT':
            return ('LShift', get_connect(a), get_connect(b))
        elif op == 'RSHIFT':
            return ('RShift', get_connect(a), get_connect(b))


def get_op(wire):
    return wire[0]


def get_operands(wire):
    if get_op(wire) == 'Not':
        return [wire[1]]
    else:
        return [wire[1], wire[2]]


def is_signal(operand):
    return isinstance(operand, int)


def has_signal(wire):
    return all(map(is_signal, get_operands(wire)))


# wire should have both signals
def compute_value(wire):
    if is_signal(wire):
        return wire
    elif get_op(wire) == 'Not':
        return ~ wire[1]
    elif get_op(wire) == 'And':
        return (wire[1] & wire[2])
    elif get_op(wire) == 'Or':
        return (wire[1] | wire[2])
    elif get_op(wire) == 'LShift':
        return (wire[1] << wire[2])
    elif get_op(wire) == 'RShift':
        return (wire[1] >> wire[2])


def resolve_signals(remaining, completed):
    while remaining:
        nremaining = {}

        for connect, wire in remaining.items():
            wire_a = wire[1] if is_signal(wire[1]) else completed.get(wire[1], wire[1])

            if get_op(wire) == 'Not':
                newire = (wire[0], wire_a)
            else:
                wire_b = wire[2] if is_signal(wire[2]) else completed.get(wire[2], wire[2])
                newire = (wire[0], wire_a, wire_b)
            
            if has_signal(newire):
                completed[connect] = compute_value(newire)
            else:
                nremaining[connect] = newire
        
        remaining = nremaining


def read_input(data):
    completed = {}
    remaining = {}

    for line in data.split('\n'):
        line = line.strip()
        wire, connect = line.split(' -> ')

        connect = get_connect(connect)
        wire = read_wire(wire)

        if is_signal(wire):
            completed[connect] = wire
        else:
            remaining[connect] = wire
    
    return completed, remaining


if __name__ == '__main__':
    puzzle = Puzzle(year=2015, day=7)

    data = '''123 -> x
        456 -> y
        x AND y -> d
        x OR y -> e
        x LSHIFT 2 -> f
        y RSHIFT 2 -> g
        NOT x -> h
        NOT y -> i'''
    
    data = puzzle.input_data

    # part 1
    completed, remaining = read_input(data)
    resolve_signals(remaining, completed)
    part1_a = completed['a']
    print(part1_a)

    # part 2
    completed, remaining = read_input(data)
    completed['b'] = part1_a
    # if b is in remaining, delete it
    if 'b' in remaining: del remaining['b']
    resolve_signals(remaining, completed)
    print(completed['a'])
