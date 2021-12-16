from aocd.models import Puzzle


if __name__ == '__main__':
    puzzle = Puzzle(year=2015, day=1)
    data = puzzle.input_data

    res = sum((1 if x == '(' else -1) for x in data)
    puzzle.answer_a = res

    floor = 0
    for i, x in enumerate(data):
        if x == '(':
            floor += 1
        else:
            floor -= 1
        if floor == -1:
            print(i+1)
            break
