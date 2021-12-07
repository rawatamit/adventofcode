from aocd.models import Puzzle


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
    
    def run(self, insts, maxop=40):
        ip = 0
        curop = 0
        output = []

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
            elif inst == 'out':
                r = args[0]
                #print(self.get_argument(r))
                output.append(self.get_argument(r))
                curop += 1
                if curop > maxop: return output
                ip += 1
            elif inst == 'jnz':
                x, y = args

                if self.get_argument(x) != 0:
                    ip += self.get_argument(y)
                else:
                    ip += 1


if __name__ == '__main__':
    puzzle = Puzzle(year=2016, day=25)
    data = puzzle.input_data

    insts = data.split('\n')

    # part 1
    #for i in range(0, 257, 2):
    for i in [180]:
        comp = Computer()
        comp.set_reg('a', i)
        output = comp.run(insts, maxop=60)

        print(f'a={i}, output={output}')
