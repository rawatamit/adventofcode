from itertools import permutations


def is_triangle(sides):
    for x, y, z in permutations(sides):
        if x + y <= z:
            return False
    return True


def part1():
    with open('d3.txt') as fin:
        count = 0
        for line in fin:
            sides = [int(x) for x in line.strip().split()]
            if is_triangle(sides):
                count += 1
        
        print(count)


def part2():
    with open('d3.txt') as fin:
        count = 0

        while True:
            set_of_3 = []
            for _ in range(3):
                line = fin.readline()
                if not line: break
                set_of_3.append([int(x) for x in line.strip().split()])
            
            if not set_of_3: break
            for index in (0, 1, 2):
                sides = []
                for row in range(3):
                    sides.append(set_of_3[row][index])
                
                if is_triangle(sides):
                    count += 1

        print(count)


if __name__ == '__main__':
    part1()
    part2()
