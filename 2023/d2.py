from aocd import get_data


def parse_game(line):
    id_str, rounds_str = line.split(':')
    rounds = []
    for round in rounds_str.split(';'):
        round_counts = {'red': 0, 'green': 0, 'blue': 0}
        for cubes in round.split(','):
            count, color = cubes.split()
            round_counts[color.strip()] = int(count.strip())
        rounds.append(round_counts)
    id = int(id_str.split()[-1])
    return id, rounds

if __name__ == '__main__':
    data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    data = get_data(year=2023, day=2)

    # part 1
    sum_ids = 0
    sum_powers = 0
    for line in data.splitlines():
        game = parse_game(line.strip())
        id, rounds = game
        correct = True
        max_cubes = {'red': 0, 'green': 0, 'blue': 0}
        for round in rounds:
            # part 2
            for color, val in max_cubes.items():
                max_cubes[color] = max(val, round[color])

            # part 1
            if round['red'] > 12 or round['green'] > 13 or round['blue'] > 14:
                correct = False
        power = 1
        for v in max_cubes.values(): power *= 1 if v == 0 else v
        sum_powers += power
        sum_ids += id if correct else 0
    print('part1', sum_ids)
    print('part2', sum_powers)

