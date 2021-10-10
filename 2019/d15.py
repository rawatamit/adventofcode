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


def make_grid(G):
    max_x = max(x for x,_ in G.keys())
    max_y = max(y for _,y in G.keys())
    min_x = min(x for x,_ in G.keys())
    min_y = min(y for _,y in G.keys())

    min_x, min_y = abs(min_x), abs(min_y)

    droid_pos = None
    oxygen_pos = None
    grid = [['#' for _ in range(max_x+min_x+1)] for _ in range(max_y+min_y+1)]

    for (x, y), v in G.items():
        if v == 'O':
            oxygen_pos = (min_x+x, min_y+y)
        grid[min_y+y][min_x+x] = v
    
    droid_pos = (min_x, min_y)
    grid[min_y][min_x] = 'D'
    return grid, droid_pos, oxygen_pos


def draw(grid):
    for row in grid:
        print(''.join(row))


def neighbors(x, y, grid):
    row = len(grid)
    col = len(grid[0])

    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]

    for i in range(len(dx)):
        nx = x + dx[i]
        ny = y + dy[i]
        if 0 <= nx < col and 0 <= ny < row:
            yield nx, ny


def path_explorer(grid, start, fn):
    Q = deque()
    seen = set()

    Q.append((start, 0))

    while Q:
        pos, steps = Q.popleft()
        x, y = pos

        if pos in seen: continue
        seen.add(pos)

        if fn((x, y), steps): return steps

        for npos in neighbors(x, y, grid):
            if grid[y][x] != '#':
                Q.append((npos, steps + 1))
    
    return -1


def shortest_path(grid, start, end):
    # data[0] is position
    fn = lambda pos, _: pos == end
    return path_explorer(grid, start, fn)


def longest_path(grid, start, end):
    max_steps = -1
    def fn(pos, steps):
        nonlocal max_steps
        max_steps = max(max_steps, steps)
    path_explorer(grid, start, fn)
    return max_steps


async def explore(input, output, cur_pos=(0, 0), G={}, seen=set()):
    cmds = [1, 2, 3, 4]

    # we are going to start exploring this node
    # mark it seen
    seen.add(cur_pos)

    for cmd in cmds:
        npos = next_position(cur_pos, cmd)

        if npos in seen: continue

        await input.put(cmd)
        status = await output.get()
        output.task_done()

        # moved one step in the requested direction
        if status == 0:
            # wall
            seen.add(npos)
            G[npos] = '#'
        else:
            if status == 2: G[npos] = 'O'
            else: G[npos] = '.'

            await explore(input, output, npos, G, seen)
            bt_cmd = backtrack_cmd(cmd)
            await input.put(bt_cmd)
            await output.get()
            output.task_done()
     
    return -1


async def remote_control(program):
    G = {}
    input = asyncio.Queue()
    output = asyncio.Queue()
    producer = asyncio.create_task(explore(input, output, (0, 0), G))
    asyncio.create_task(IntCodeComputerMk2(program, input, output).execute())
    await asyncio.gather(producer)
    await input.join()
    await output.join()
    return make_grid(G)


async def main():
    with open('d15.txt') as fin:
        program = [int(x) for x in fin.readline().split(',') if x]
    
    ## part 1
    grid, droid_pos, oxygen_pos = await remote_control(program)

    # draw(grid)
    x = shortest_path(grid, droid_pos, oxygen_pos)
    print(x)

    # part 2
    x = longest_path(grid, oxygen_pos, None)
    print(x)

asyncio.run(main())
