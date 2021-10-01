from itertools import permutations
from collections import deque
import asyncio
from intcode_computer import IntCodeComputerMk1

class IntCodeComputerMk0:
    def __init__(self, program, input=None, output=None):
        self.ip = 0
        self.program = program[:]
        self.input = input
        self.output = output

    def get_operation(self, opcode):
        return opcode % 100

    def get_mode(self, opcode, pos):
        op_div = 10 ** (pos + 1)
        return 0 if opcode < op_div else (opcode // op_div) % 10 # mode 0 by default 
    
    def get_address(self, pos, mode):
        if mode == 2:
            return self.program[self.ip + pos] + self.relative_base
        elif mode == 1:
            return self.ip + pos
        elif mode == 0:
            return self.program[self.ip + pos]
        return -1

    def get_operand(self, opcode, pos):
        mode = self.get_mode(opcode, pos)
        addr = self.get_address(pos, mode)
        return self.program[addr]

    def get_input(self):
        if self.input is None:
            return input('Enter value: ')
        else:
            return next(self.input)

    async def execute(self):
        self.ip = 0
        retval = -1

        while self.ip < len(self.program):
            op = self.program[self.ip]
            operation = self.get_operation(op)

            if operation == 1:
                arg1 = self.get_operand(op, 1)
                arg2 = self.get_operand(op, 2)
                self.program[self.program[self.ip + 3]] = arg1 + arg2
                self.ip += 4
            elif operation == 2:
                arg1 = self.get_operand(op, 1)
                arg2 = self.get_operand(op, 2)
                self.program[self.program[self.ip + 3]] = arg1 * arg2
                self.ip += 4
            elif operation == 3:
                x = await self.input.get()
                self.program[self.program[self.ip + 1]] = int(x)
                self.ip += 2
            elif operation == 4:
                retval = self.get_operand(op, 1)
                await self.output.put(retval)
                self.ip += 2
            elif operation == 5:
                arg1 = self.get_operand(op, 1)
                arg2 = self.get_operand(op, 2)
                if arg1 != 0: self.ip = arg2
                else: self.ip += 3
            elif operation == 6:
                arg1 = self.get_operand(op, 1)
                arg2 = self.get_operand(op, 2)
                if arg1 == 0: self.ip = arg2
                else: self.ip += 3
            elif operation == 7:
                arg1 = self.get_operand(op, 1)
                arg2 = self.get_operand(op, 2)
                self.program[self.program[self.ip + 3]] = 1 if arg1 < arg2 else 0
                self.ip += 4
            elif operation == 8:
                arg1 = self.get_operand(op, 1)
                arg2 = self.get_operand(op, 2)
                self.program[self.program[self.ip + 3]] = 1 if arg1 == arg2 else 0
                self.ip += 4
            elif operation == 99:
                return retval
            else:
                raise Exception(f'unknown opcode: {operation} at ip: {self.ip}')

# part 1 below
def run_amplifier(program, phase, input_signal):
    return IntCodeComputerMk1(program, iter([phase, input_signal])).execute()[-1]

def run_amplifier_seq(program, phases, first_input):
    output_ = first_input

    for phase in phases:
        output_ = run_amplifier(program, phase, output_)
    
    return output_

def find_max_thrust(program):
    max_output = 0
    for phases in permutations(range(5)):
        max_output = max(max_output, run_amplifier_seq(program, phases, 0))
    return max_output

# part 2 below
async def run_feedback_loop(program, phases):
    qAE = asyncio.Queue()

    qAB = asyncio.Queue()
    await qAE.put(phases[0])
    await qAE.put(0)
    ampA = IntCodeComputerMk0(program, qAE, qAB)

    qBC = asyncio.Queue()
    await qAB.put(phases[1])
    ampB = IntCodeComputerMk0(program, qAB, qBC)

    qCD = asyncio.Queue()
    await qBC.put(phases[2])
    ampC = IntCodeComputerMk0(program, qBC, qCD)
    
    qDE = asyncio.Queue()
    await qCD.put(phases[3])
    ampD = IntCodeComputerMk0(program, qCD, qDE)

    await qDE.put(phases[4])
    ampE = IntCodeComputerMk0(program, qDE, qAE)

    x = await asyncio.gather(ampA.execute(), ampB.execute(),
                             ampC.execute(), ampD.execute(),
                             ampE.execute())
    return x[-1]

async def find_max_thrust_feedback(program):
    max_output = 0
    for phases in permutations(range(5, 10)):
        cur_output = await run_feedback_loop(program, phases)
        max_output = max(max_output, cur_output)
    return max_output

if __name__ == '__main__':
    with open('d7.txt') as fin:
        program = [int(x) for x in fin.readline().split(',') if x.strip()]
    
    # x = run_amplifier(program, 0, 0)
    # x = run_amplifier_seq(program, [1,0,4,3,2], 0)
    # x = find_max_thrust(program)
    # print(x)

    ## part 2
    x = asyncio.run(find_max_thrust_feedback(program))
    print(x)
