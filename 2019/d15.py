import asyncio
from collections import deque
from intcode_computer import IntCodeComputerMk2


def tuple_add(ta, tb):
    return (ta[0] + tb[0], ta[1] + tb[1])


def next_position(cur_pos, cmd):
    cmd_map = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}
    return tuple_add(cmd_map[cmd], cur_pos)


def backtrack_cmd(cmd):
    return {1: 2, 2: 1, 3: 4, 4: 3}[cmd]


async def explore(input, output, cur_pos=(0, 0), steps=0, seen=set()):
    cmds = [1, 2, 3, 4]

    # we are going to start exploring this node
    # mark it seen
    seen.add(cur_pos)

    for cmd in cmds:
        npos = next_position(cur_pos, cmd)
        if npos == (0, 0): input.task_done()

        if npos in seen: continue

        await input.put(cmd)
        status = await output.get()

        # moved one step in the requested direction
        if status == 0:
            # wall
            seen.add(npos)
        else:
            await explore(input, output, npos, steps + 1, seen)
            bt_cmd = backtrack_cmd(cmd)
            await input.put(bt_cmd)
            await output.get()
     
    return -1


async def remote_control(program):
    input = asyncio.Queue()
    output = asyncio.Queue()

    x = await asyncio.gather(
        IntCodeComputerMk2(program, input, output).execute(),
        explore(input, output, (0, 0)))
    await input.join()


async def main():
    with open('d15.txt') as fin:
        program = [int(x) for x in fin.readline().split(',') if x]
    
    ## part 1
    steps = await remote_control(program)
    print(steps)

asyncio.run(main())
