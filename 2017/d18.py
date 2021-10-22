from collections import defaultdict
import queue
import threading


class CPU:
    def __init__(self) -> None:
        self.regs = defaultdict(int)
        self.last_sound = 0
    
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
    
    def add(self, r1, r2):
        self.regs[r1] += self.get_value(r2)
    
    def mul(self, r1, r2):
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
            else:
                fn = getattr(self, op)
                ret = fn(*args)
                if op == 'rcv' and ret: break
                pc += 1


class CPU2(CPU):
    def __init__(self, pc_id, input, output) -> None:
        super().__init__()
        self.regs['p'] = pc_id
        self.pc_id = pc_id
        self.input = input
        self.output = output
        self.send_count = 0
    
    def snd(self, reg):
        self.send_count += 1
        self.output.put_nowait(self.regs[reg])
    
    def rcv(self, reg):
        self.regs[reg] = self.input.get(block=True, timeout=1)
        self.input.task_done()


def make_cpu(pc_id, input, output, insts):
    pc = CPU2(pc_id, input, output)

    try:
        pc.run(insts[:])
    except Exception:
        if pc_id == 1:
            print(f'pc 1 sent {pc.send_count} messages')


def part2(insts):
    # act as input for pc1 and output for pc2
    q1 = queue.Queue()
    # act as input for pc2 and output for pc1
    q2 = queue.Queue()

    threading.Thread(target=make_cpu, args=(0, q1, q2, insts)).start()
    threading.Thread(target=make_cpu, args=(1, q2, q1, insts)).start()


def main():
    insts = []
    with open('d18.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                insts.append(line.split())
    
    # part 1
    CPU().run(insts)

    # part 2
    part2(insts)


main()
