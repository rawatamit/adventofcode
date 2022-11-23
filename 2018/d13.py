from aocd import get_data
from heapq import heapify, heappop
from collections import defaultdict


class Car:
    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir
        self.next_turn = 0

    def __repr__(self):
        return str(self)
    def __str__(self):
        return f'Car<pos={self.pos}, dir={self.dir}, emoji={self.emoji()}>'

    def emoji(self):
        return {1+0j: '>', -1+0j: '<', 0+1j: 'v', 0-1j: '^'}[self.dir]

    def turn_right(self):
        self.dir *= 0+1j

    def turn_left(self):
        self.dir *= 0-1j

    def move(self):
        self.pos += self.dir

    def straight(self):
        pass

    def intersection(self):
        if self.next_turn == 0:
            self.turn_left()
        elif self.next_turn == 1:
            self.straight()
        elif self.next_turn == 2:
            self.turn_right()

        self.next_turn = (self.next_turn + 1) % 3


def move_cars(grid, cars, cars_crashed, find_first_crash):
    qu = [(car.pos.imag, car.pos.real, i, car)
           for i, car in enumerate(cars)]
    heapify(qu)

    survive = [car for car in cars if not car in cars_crashed]
    if len(survive) == 1:
        print(f'car at pos {survive[0].pos}')
        return 1

    while qu:
        _, _, _, car = heappop(qu)
        if car in cars_crashed: continue

        # move car, and check for collision
        car.move()
        car_pos = defaultdict(set)
        for ncar in cars:
            if ncar in cars_crashed: continue
            if ncar.pos in car_pos:
                #print(f'found crash {ncar.pos}, between {ncar} and {car_pos[ncar.pos]}')
                if find_first_crash:
                    return ncar.pos
                else:
                    # save the cars that are crashed
                    cars_crashed.add(ncar)
                    cars_crashed.update(car_pos[ncar.pos])
            else:
                car_pos[ncar.pos].add(ncar)

        if car in cars_crashed:
            continue

        # check where the car is now, and change directions if needed
        y, x = int(car.pos.imag), int(car.pos.real)
        cell = grid[y][x]
        emoji = car.emoji()
        if cell == '/':
            if emoji in ('^', 'v'):
                car.turn_right()
            elif emoji in ('<', '>'):
                car.turn_left()
        elif cell == '\\':
            if emoji in ('^', 'v'):
                car.turn_left()
            elif emoji in ('<', '>'):
                car.turn_right()
        elif cell == '+':
            car.intersection()


def draw_grid(grid, cars, cars_crashed):
    car_pos = {car.pos: car.emoji()
                for car in cars if car not in cars_crashed}
    ngrid = []
    for y, row in enumerate(grid):
        nrow = []
        ngrid.append(nrow)
        for x, cell in enumerate(row):
            ncell = car_pos.get(complex(x, y), cell)
            nrow.append(ncell)

    for row in ngrid:
        print(''.join(row))


if __name__ == '__main__':
    data = r'''/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/'''

    data = '''/>-<\\  
|   |  
| /<+-\\
| | | v
\>+</ |
  |   ^
  \<->/'''
    data = get_data(year=2018, day=13)
    #print(data)

    grid = [list(s.rstrip()) for s in data.splitlines()]
    cars = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '>':
                cars.append(Car(complex(x, y), 1+0j))
                grid[y][x] = '-'
            elif cell == '<':
                cars.append(Car(complex(x, y), -1+0j))
                grid[y][x] = '-'
            elif cell == 'v':
                cars.append(Car(complex(x, y), 0+1j))
                grid[y][x] = '|'
            elif cell == '^':
                cars.append(Car(complex(x, y), 0-1j))
                grid[y][x] = '|'

    part1 = False
    cars_crashed = set()
    if part1:
        crash = False
        while not crash:
            #draw_grid(grid, cars)
            #print('**************')
            crash = move_cars(grid, cars, cars_crashed, True)
        #draw_grid(grid, cars)
    else:
        for _ in range(20000):
            #draw_grid(grid, cars, cars_crashed)
            #print('**************')
            ret = move_cars(grid, cars, cars_crashed, False)
            if ret == 1: break
        #draw_grid(grid, cars, cars_crashed)
