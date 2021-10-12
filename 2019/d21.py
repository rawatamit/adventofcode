import asyncio
from intcode_computer import IntCodeComputerMk2


async def put_stringln(s, input):
    for c in s:
        await input.put(ord(c))
    await input.put(ord('\n'))


async def send_recv_instructions(instructions, input, output):
    while output.qsize() > 0:
        x = await output.get()
        print(chr(x), end='')
        output.task_done()
    
    for inst in instructions:
        await put_stringln(inst, input)

    damage = -1
    while True:
        x = await output.get()
        output.task_done()

        if x is None: return damage

        if len(str(x)) > 3: damage = x
        else: print(chr(x), end='')
    
    return damage


async def play_with_droid(instructions, program):
    input = asyncio.Queue()
    output = asyncio.Queue()

    tasks = [send_recv_instructions(instructions, input, output),
             IntCodeComputerMk2(program, input, output).execute()]
    ret = await asyncio.gather(*tasks)

    await input.join()
    await output.join()
    return ret


def generate_program(registers, opcodes, insts, i, length):
    # generates program of length such that each instruction
    # is of the form OP R1 R2

    if i >= length:
        insts[i] = 'WALK'
        # print(insts)
        return
    
    for opcode in opcodes:
        for r1 in registers:
            if r1 == 'J': continue
            for r2 in registers:
                if r1 == r2: continue
                cur = f'{opcode} {r1} {r2}'
                save = insts[i]
                insts[i] = cur
                generate_program(registers, opcodes, insts, i+1, length)
                insts[i] = save


def gen_part1():
    registers = ['T', 'J', 'A', 'B', 'C', 'D']
    opcodes = ['AND', 'OR', 'NOT']
    length = 5

    generate_program(registers, opcodes, [None for _ in range(length+1)], 0, length)


async def main():
    with open('d21.txt') as fin:
        program = [int(x) for x in fin.readline().split(',') if x]
    
    # part 1
    # instructions = [
    #     'OR A T',
    #     'AND B T',
    #     'AND C T',
    #     'NOT T J',
    #     'AND D J',
    #     'WALK']
    # ret = await play_with_droid(instructions, program)
    # print(ret)

    # part 2
    instructions = [
        'OR A T',
        'AND B T',
        'AND C T',
        'NOT T J',
        'AND D J',
        'RUN']
    ret = await play_with_droid(instructions, program)
    print(ret)

asyncio.run(main())
