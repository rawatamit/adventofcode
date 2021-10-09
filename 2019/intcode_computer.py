import asyncio

class IntCodeComputerMk1:
    def __init__(self, program, input=None):
        self.ip = 0
        self.program = program[:]
        self.input = input
        self.output = []

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

    def execute(self):
        self.ip = 0

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
                x = self.get_input()
                self.program[self.program[self.ip + 1]] = int(x)
                self.ip += 2
            elif operation == 4:
                self.output.append(self.get_operand(op, 1))
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
                return self.output
            else:
                raise Exception(f'unknown opcode: {operation} at ip: {self.ip}')


class IntCodeComputerMk2:
    def __init__(self, program, input=None, output=None):
        self.memory = {}
        self.ip = 0
        self.relative_base = 0
        self.program = program[:]
        self.input = input
        self.output = output

    def read_memory(self, addr):
        if addr not in self.memory:
            self.memory[addr] = 0
        return self.memory[addr]

    def write_memory(self, addr, value):
        self.memory[addr] = value

    def read_data(self, addr):
        if addr < 0:
            raise('cannot access negative memory address')

        if addr >= 0 and addr < len(self.program):
            return self.program[addr]
        else:
            return self.read_memory(addr)

    def save_data(self, addr, value):
        if addr < 0:
            raise('cannot access negative memory address')

        if addr >= 0 and addr < len(self.program):
            self.program[addr] = value
        else:
            self.write_memory(addr, value)

    async def get_input(self):
        if self.input is None:
            return input('Enter value: ')
        else:
            return await self.input.get()

    def get_operation(self, opcode):
        return opcode % 100 # last two digits of opcode

    def get_mode(self, opcode, pos):
        op_div = 10 ** (pos + 1)
        return 0 if opcode < op_div else (opcode // op_div) % 10 # mode 0 by default 
    
    def get_address(self, pos, mode):
        if mode == 2:
            return self.read_data(self.ip + pos) + self.relative_base
        elif mode == 1:
            return self.ip + pos
        elif mode == 0:
            return self.read_data(self.ip + pos)
        return -1

    def get_operand(self, opcode, pos):
        mode = self.get_mode(opcode, pos)
        addr = self.get_address(pos, mode)
        return self.read_data(addr)

    def get_write_address(self, opcode, pos):
        mode = self.get_mode(opcode, pos)
        return self.get_address(pos, mode)

    async def execute(self):
        self.ip = 0
        self.memory = {}
        self.relative_base = 0

        while self.ip < len(self.program):
            op = self.program[self.ip]
            operation = self.get_operation(op)

            if operation == 1:
                arg1 = self.get_operand(op, 1)
                arg2 = self.get_operand(op, 2)
                addr = self.get_write_address(op, 3)
                self.save_data(addr, arg1 + arg2)
                self.ip += 4
            elif operation == 2:
                arg1 = self.get_operand(op, 1)
                arg2 = self.get_operand(op, 2)
                addr = self.get_write_address(op, 3)
                self.save_data(addr, arg1 * arg2)
                self.ip += 4
            elif operation == 3:
                x = await self.get_input()
                addr = self.get_write_address(op, 1)
                self.save_data(addr, int(x))
                self.ip += 2
            elif operation == 4:
                output = self.get_operand(op, 1)
                await self.output.put(output)
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
                addr = self.get_write_address(op, 3)
                self.save_data(addr, 1 if arg1 < arg2 else 0)
                self.ip += 4
            elif operation == 8:
                arg1 = self.get_operand(op, 1)
                arg2 = self.get_operand(op, 2)
                addr = self.get_write_address(op, 3)
                self.save_data(addr, 1 if arg1 == arg2 else 0)
                self.ip += 4
            elif operation == 9:
                self.relative_base += self.get_operand(op, 1)
                self.ip += 2
            elif operation == 99:
                return 0
            else:
                raise Exception('unknown opcode: {}'.format(op))
