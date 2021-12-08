class Computer:
    def __init__(self) -> None:
        self.regs = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    
    def get_argument(self, x):
        if x in self.regs:
            return self.regs[x]
        return int(x)
    
    def set_reg(self, r, value):
        assert r in self.regs
        self.regs[r] = value
    
    def run(self, insts):
        ip = 0

        while ip < len(insts):
            opcode = insts[ip]
            inst, args = opcode.split()[0], opcode.split()[1:]

            if inst == 'cpy':
                x, y = args
                self.set_reg(y, self.get_argument(x))
                ip += 1
            elif inst == 'inc':
                r = args[0]
                self.set_reg(r, self.get_argument(r) + 1)
                ip += 1
            elif inst == 'dec':
                r = args[0]
                self.set_reg(r, self.get_argument(r) - 1)
                ip += 1
            elif inst == 'jnz':
                x, y = args

                if self.get_argument(x) != 0:
                    ip += self.get_argument(y)
                else:
                    ip += 1


if __name__ == '__main__':
    with open('d12.txt') as fin:
        insts = fin.read().split('\n')
        # part 1
        comp = Computer()
        comp.run(insts)
        print(comp.regs)

        # part 2
        comp = Computer()
        comp.regs['c'] = 1
        comp.run(insts)
        print(comp.regs)