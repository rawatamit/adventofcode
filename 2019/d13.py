import asyncio
from intcode_computer import IntCodeComputerMk2


async def block_tiles(output):
    count = 0
    next_i = 2
    for i in range(output.qsize()):
        x = await output.get()
        if i == next_i:
            if x == 2: count += 1
            next_i += 3
    return count


def update_screen(string_screen, screen):
    tile_map = {0: ' ', 1: '#', 2: '.', 3: '-', 4: 'o'}

    for (x, y), d in screen.items():
        string_screen[y][x] = tile_map[d]


def build_screen(screen, score):
    max_x = max(x for x,_ in screen.keys())
    max_y = max(y for _,y in screen.keys())

    s = [[' ' for _ in range(max_x+1)] for _ in range(max_y+1)]
    update_screen(s, screen)
    return s


def draw(screen, score):
    for row in screen:
        print(''.join(row))
    print(f'SCORE: {score}')


async def player_input(async_input):
    x = input('Enter joystick value: ')
    await async_input.put(int(x))


async def play_moves(input, output):
    screen = {}
    string_screen = None

    while True:
        x = await output.get()
        y = await output.get()
        d = await output.get()

        if (x, y) == (-1, 0): score = d
        else: screen[(x, y)] = d

        if d == 3: print(f'paddle at ({x},{y})')
        if d == 4: print(f'ball at ({x},{y})')

        # print the initial game screen
        if output.qsize() == 0 and string_screen is None:
            string_screen = build_screen(screen, score)
            draw(string_screen, score)
            screen = {}
            await player_input(input)
        elif output.qsize() == 0:
            update_screen(string_screen, screen)
            draw(string_screen, score)
            screen = {}
            await player_input(input)


async def play_text_game(program):
    program[0] = 2
    input = asyncio.Queue()
    output = asyncio.Queue()
    await asyncio.gather(
        IntCodeComputerMk2(program, input=input, output=output).execute(),
        play_moves(input, output))


async def play_ai_moves(input, output):
    score = 0
    ball = None
    paddle = None

    while True:
        x = await output.get()
        y = await output.get()
        d = await output.get()

        if (x, y) == (-1, 0): score = d
        if d == 3: paddle = (x, y)
        if d == 4: ball = (x, y)

        if output.qsize() == 0:
            print(f'SCORE: {score}')
            # waiting for input
            if paddle[0] < ball[0]:
                await input.put(1)
            elif paddle[0] > ball[0]:
                await input.put(-1)
            else:
                await input.put(0)


async def play_ai_game(program):
    program[0] = 2
    input = asyncio.Queue()
    output = asyncio.Queue()
    await asyncio.gather(
        IntCodeComputerMk2(program, input=input, output=output).execute(),
        play_ai_moves(input, output))
 

async def main():
    with open('d13.txt') as fin:
        program = [int(x) for x in fin.readline().split(',') if x]
    
    ## part 1
    # output = asyncio.Queue()
    # await IntCodeComputerMk2(program, input=None, output=output).execute()
    # print(await block_tiles(output))

    ## part 2
    await play_ai_game(program)


asyncio.run(main())
