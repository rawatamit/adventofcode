import asyncio
from collections import deque
from intcode_computer import IntCodeComputerMk2


async def put_stringln(s, input):
    for c in s:
        await input.put(ord(c))
    await input.put(ord('\n'))


import sys
async def explore(input_q, output):
    inputs = [
        'east',
        'take jam',
        'south',
        'take shell',
        ]
    
    cur_output = deque()
    while True:
        if ''.join(cur_output) == "Command?":
            cur_output = deque()
            s = input('input: ')
            await put_stringln(s, input_q)

        #while output.qsize() > 0:
        x = await output.get()
        output.task_done()
        if x is None: break
        
        print(chr(x), end='')
        if len(cur_output) > 8: cur_output.popleft()
        if x != 10: cur_output.append(chr(x))


async def play_with_droid(program):
    input = asyncio.Queue()
    output = asyncio.Queue()

    # await put_stringln('east', input)
    # await put_stringln('take jam', input)
    # await put_stringln('inv', input)

    tasks = [explore(input, output),
             IntCodeComputerMk2(program, input, output).execute()]
    ret = await asyncio.gather(*tasks)

    await input.join()
    await output.join()
    return ret


async def main():
    with open('d25.txt') as fin:
        program = [int(x) for x in fin.readline().split(',') if x]
    
    ret = await play_with_droid(program)
    print(ret)


asyncio.run(main())
