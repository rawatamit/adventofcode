from aocd import get_data

def opponent(play):
    return {'A': 'R', 'B': 'P', 'C': 'S'}[play]

def me_part1(play):
    return {'X': 'R', 'Y': 'P', 'Z': 'S'}[play]

def me_part2(oplay, res):
    play_list = [(round_score(mplay, oplay), mplay)
        for mplay in ('R', 'P', 'S')]
    play_list.sort()
    idx = {'X': 0, 'Y': 1, 'Z': 2}
    return play_list[idx[res]][1]

def shape_score(play):
    return {'R': 1, 'P': 2, 'S': 3}[play]

def round_score(mplay, oplay):
    # me vs opponent
    score_map = {'R': {'R': 3, 'P': 0, 'S': 6},
            'P': {'R': 6, 'P': 3, 'S': 0},
            'S': {'R': 0, 'P': 6, 'S': 3}}
    return score_map[mplay][oplay] + shape_score(mplay)

if __name__ == '__main__':
    data = 'A Y\nB X\nC Z'
    data = get_data(year=2022, day=2)
    strategy = [s.split() for s in data.splitlines()]
    print(sum(round_score(me_part1(mplay), opponent(oplay))
            for oplay, mplay in strategy))

    print(sum(round_score(me_part2(opponent(oplay), res), opponent(oplay))
            for oplay, res in strategy))

