import json
from collections import defaultdict


class VM:
    def __init__(self, regs=[0, 0, 0, 0]):
        assert len(regs) == 4
        self.regs = regs[:]
    
    def registers(self):
        return self.regs

    def op_immediate(self, r1, val, r3, op_fn=None):
        self.regs[r3] = op_fn(self.regs[r1], val)
    
    def op_register(self, r1, r2, r3, op_fn=None):
        self.regs[r3] = op_fn(self.regs[r1], self.regs[r2])

    def addr(self, r1, r2, r3):
        self.op_register(r1, r2, r3, op_fn=lambda x, y: x+y)
    def addi(self, r1, val, r3):
        self.op_immediate(r1, val, r3, op_fn=lambda x, y: x+y)

    def mulr(self, r1, r2, r3):
        self.op_register(r1, r2, r3, op_fn=lambda x, y: x*y)
    def muli(self, r1, val, r3):
        self.op_immediate(r1, val, r3, op_fn=lambda x, y: x*y)

    def banr(self, r1, r2, r3):
        self.op_register(r1, r2, r3, op_fn=lambda x, y: x&y)
    def bani(self, r1, val, r3):
        self.op_immediate(r1, val, r3, op_fn=lambda x, y: x&y)

    def borr(self, r1, r2, r3):
        self.op_register(r1, r2, r3, op_fn=lambda x, y: x|y)
    def bori(self, r1, val, r3):
        self.op_immediate(r1, val, r3, op_fn=lambda x, y: x|y)

    def setr(self, r1, _, r3):
        self.regs[r3] = self.regs[r1]
    def seti(self, val, _, r3):
        self.regs[r3] = val
    
    def gtir(self, val, r2, r3):
        self.regs[r3] = 1 if val > self.regs[r2] else 0
    def gtri(self, r1, val, r3):
        self.regs[r3] = 1 if self.regs[r1] > val else 0
    def gtrr(self, r1, r2, r3):
        self.regs[r3] = 1 if self.regs[r1] > self.regs[r2] else 0

    def eqir(self, val, r2, r3):
        self.regs[r3] = 1 if val == self.regs[r2] else 0
    def eqri(self, r1, val, r3):
        self.regs[r3] = 1 if self.regs[r1] == val else 0
    def eqrr(self, r1, r2, r3):
        self.regs[r3] = 1 if self.regs[r1] == self.regs[r2] else 0


def find_opcode_mapping(opcode_map):
    # invariant: Q only has op which have a 1-1 mapping
    Q = [op
        for op, opcode in opcode_map.items()
        if len(opcode) == 1]
    
    mapping = {}

    while Q:
        op_set = Q.pop()
        opcode = opcode_map[op_set].pop()
        mapping[opcode] = op_set

        for op, opcodes in opcode_map.items():
            if op not in mapping and opcode in opcodes:
                opcodes.remove(opcode)
                if len(opcodes) == 1:
                    Q.append(op)
     
    return mapping


def part1(states):
    fns = ['addr', 'addi', 'mulr', 'muli',
           'banr', 'bani', 'borr', 'bori',
           'setr', 'seti',
           'gtir', 'gtri', 'gtrr',
           'eqir', 'eqri', 'eqrr']
    
    three_or_more = 0
    opcode_map = defaultdict(set)

    for before, after, inst in states:
        count = 0
        opcode, a, b, c = inst
        for fn in fns:
            vm = VM(before)
            # don't use opcode
            getattr(VM, fn)(vm, a, b, c)
            if vm.registers() == after:
                opcode_map[fn].add(opcode)
                count += 1
        
        if count >= 3:
            three_or_more += 1

    mapping = find_opcode_mapping(opcode_map)
    return three_or_more, mapping


def part2(program, opcode_map):
    vm = VM()

    for opcode, a, b, c in program:
        getattr(VM, opcode_map[opcode])(vm, a, b, c)

    return vm.registers()


def main():
    program = []
    states = []

    with open('d16.txt') as fin:
        while True:
            line = fin.readline()
            if not line: break
            line = line.strip()

            if line.startswith('Before'):
                # read states
                before = json.loads(line.split(':')[1])
                inst = [int(x) for x in fin.readline().split()]
                after = json.loads(fin.readline().split(':')[1])
                states.append((before, after, inst))
            elif line:
                # read program
                program.append([int(x) for x in line.split()])

            # skip whitespace
    
    # part 1
    three_or_more, opcode_map = part1(states)
    print(three_or_more)

    # part 2
    regs = part2(program, opcode_map)
    print(regs)


main()
