import asyncio
from intcode_computer import IntCodeComputerMk2


async def read_camera(output):
    row = []
    G = []

    while output.qsize():
        x = await output.get()

        if chr(x) == '\n':
            if row: G.append(row)
            row = []
        else:
            row.append(chr(x))
    
    return G


async def read_scaffolding(program):
    output = asyncio.Queue()
    ret = await asyncio.gather(
                IntCodeComputerMk2(program, input=None, output=output).execute(),
                read_camera(output))
    return ret[1]


def draw(G):
    for row in G:
        print(''.join(row))


def neighbors(x, y, G):
    row = len(G)
    col = len(G[0])

    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]

    for i in range(len(dx)):
        nx = x + dx[i]
        ny = y + dy[i]
        if 0 <= nx < col and 0 <= ny < row:
            yield nx, ny


def count_scaffold(x, y, G):
    count = 1 if G[y][x] == '#' else 0
    for nx, ny in neighbors(x, y, G):
        if G[ny][nx] == '#':
            count += 1
    return count


def scaffold_intersections(G):
    ret = []
    for y in range(len(G)):
        for x in range(len(G[0])):
            if count_scaffold(x, y, G) == 5:
                ret.append((x, y))
    return ret


async def put_stringln(s, input):
    for c in s:
        await input.put(ord(c))
    await input.put(ord('\n'))


async def visit_scaffold(input, output):
    A = 'R,6,L,8,R,10'
    B = 'L,8,R,4,R,4,R,6'
    C = 'R,12,R,4,R,10,R,12'

    movement = 'C,A,C,B,C,A,B,C,A,B'

    while output.qsize() > 0:
        x = await output.get()
        print(chr(x), end=' ')
 
    await put_stringln(movement, input)
    for fn in (A, B, C):
        await put_stringln(fn, input)
    await put_stringln('N', input)

    # print('after providing input')
    # while output.qsize() > 0:
    #     print(chr(await output.get()), end=' ')


    print(await output.get())
    # print(await output.get())


async def part2(program):
    input = asyncio.Queue()
    output = asyncio.Queue()
    ret = await asyncio.gather(
                IntCodeComputerMk2(program, input, output).execute(),
                visit_scaffold(input, output))
    return ret


async def main():
    with open('d17.txt') as fin:
        program = [int(x) for x in fin.readline().split(',') if x]
    
    # part 1
    # G = await read_scaffolding(program)
    # draw(G)
    # intersections = scaffold_intersections(G)
    # y = sum(x * y for (x, y) in intersections)
    # print(y)

    # part 2
    # NOTE: had to hack into computer output as
    # the program didn't play well with waiting
    program[0] = 2
    x = await part2(program)
    print(x)
 
asyncio.run(main())
