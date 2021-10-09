import asyncio
from intcode_computer import IntCodeComputerMk2


async def drone_output(x, y, program):
    input = asyncio.Queue()
    output = asyncio.Queue()
    await input.put(x)
    await input.put(y)
    ret = await asyncio.gather(
                IntCodeComputerMk2(program, input=input, output=output).execute(),
                output.get())
    return ret[1]


async def trace_pull(program):
    count = 0
    for x in range(50):
        for y in range(50):
            count += await drone_output(x, y, program)
    return count


async def main():
    with open('d19.txt') as fin:
        program = [int(x) for x in fin.readline().split(',') if x]
    
    # part 1
    x = await trace_pull(program)
    print(x)


asyncio.run(main())
