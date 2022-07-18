from aocd import get_data

class VM:
    def __init__(self, insts) -> None:
        self.insts = insts
        self.reg = {'a': 0, 'b': 0}
    
    def run(self):
        pc = 0
        while pc < len(self.insts):
            op = self.insts[pc][0]
            if op == 'hlf':
                arg = self.insts[pc][1]
                self.reg[arg] //= 2
                pc += 1
            elif op == 'tpl':
                arg = self.insts[pc][1]
                self.reg[arg] *= 3
                pc += 1
            elif op == 'inc':
                arg = self.insts[pc][1]
                self.reg[arg] += 1
                pc += 1
            elif op == 'jmp':
                arg = self.insts[pc][1]
                pc += int(arg)
            elif op == 'jie':
                arg1 = self.insts[pc][1]
                arg2 = self.insts[pc][2]
                if self.reg[arg1] % 2 == 0:
                    pc += int(arg2)
                else:
                    pc += 1
            elif op == 'jio':
                arg1 = self.insts[pc][1]
                arg2 = self.insts[pc][2]
                if self.reg[arg1] == 1:
                    pc += int(arg2)
                else:
                    pc += 1


if __name__ == '__main__':
    data = '''
    inc a
    jio a, +2
    tpl a
    inc a
    '''.strip()
    data = get_data(year=2015, day=23)
    insts = []
    for line in data.splitlines():
        if ',' in line:
            op, arg1, arg2 = line.split()
            insts.append((op, arg1[:-1], arg2))
        else:
            op, arg = line.split()
            insts.append((op, arg))
    
    vm = VM(insts)
    vm.reg['a'] = 1
    vm.run()
    print(vm.reg)
