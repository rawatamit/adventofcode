from collections import defaultdict


class CPU:
    def __init__(self) -> None:
        self.regs = defaultdict(int)
        self.mul_count = 0
    
    def snd(self, reg):
        self.last_sound = self.regs[reg]
        print(f'play sound with freq {self.regs[reg]}')
    
    def rcv(self, reg):
        if self.regs[reg] != 0:
            print(f'recovering last sound {self.last_sound}')
            return True
        return False
    
    def get_value(self, arg):
        try:
            return int(arg)
        except ValueError:
            return self.regs[arg]
    
    def set(self, r1, r2):
        self.regs[r1] = self.get_value(r2)

    def sub(self, r1, r2):
        self.regs[r1] -= self.get_value(r2)
    
    def add(self, r1, r2):
        self.regs[r1] += self.get_value(r2)
    
    def mul(self, r1, r2):
        self.mul_count += 1
        self.regs[r1] *= self.get_value(r2)
    
    def mod(self, r1, r2):
        self.regs[r1] %= self.get_value(r2)
    
    def run(self, insts):
        pc = 0

        while 0 <= pc < len(insts):
            inst = insts[pc]
            op, args = inst[0], inst[1:]

            if op == 'jgz':
                pc += self.get_value(args[1]) if self.get_value(args[0]) > 0 else 1
            elif op == 'jnz':
                pc += self.get_value(args[1]) if self.get_value(args[0]) != 0 else 1
            else:
                fn = getattr(self, op)
                fn(*args)
                pc += 1


class CPU2(CPU):
    def __init__(self) -> None:
        super().__init__()
        self.regs['a'] = 1


def main():
    insts = []
    with open('d23.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                insts.append(line.split())
    
    # part 1
    pc = CPU()
    pc.run(insts)
    print(pc.mul_count)

    # part 2 in d23_p2.c, this is VERY inefficient
    pc = CPU2()
    pc.run(insts)
    print(pc.regs)


main()
