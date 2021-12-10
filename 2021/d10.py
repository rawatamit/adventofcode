from aocd.models import Puzzle


def get_points(c):
    return {')': 3, ']': 57, '}': 1197, '>': 25137}[c]


def is_opening(c):
    return c in ('(', '[', '{', '<')


def is_closing(c):
    return c in (')', ']', '}', '>')


def get_closing(opening):
    return {'(': ')', '[': ']',
            '{': '}', '<': '>'}[opening]


def is_match(opening, closing):
    return get_closing(opening) == closing


def is_corrupted_and_score(s):
    st = []
    for c in s:
        if is_opening(c):
            st.append(c)
        elif is_closing(c):
            if not st:
                return True, get_points(c), []
            
            opening = st.pop()
            if not is_match(opening, c):
                return True, get_points(c), []
    return False, 0, st


def autocomplete(line, st):
    complete = [get_closing(x) for x in st[::-1]]
    points = {')': 1, ']': 2, '}': 3, '>': 4}
    score = 0
    for c in complete:
        score = 5 * score + points[c]
    return score
 

if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=10)
    data = puzzle.input_data

    lines = [
        '[({(<(())[]>[[{[]{<()<>>',
        '[(()[<>])]({[<{<<[]>>(',
        '{([(<{}[<>[]}>{[]{[(<()>',
        '(((({<>}<{<{<>}{[]{[]{}',
        '[[<[([]))<([[{}[[()]]]',
        '[{[{({}]{}}([{[{{{}}([]',
        '{<[[]]>}<{[{[{[]{()[[[]',
        '[<(<(<(<{}))><([]([]()',
        '<{([([[(<>()){}]>(<<{{',
        '<{([{{}}[<[[[<>{}]]]>[]]']
    
    lines = data.split('\n')

    total_score = 0
    autocomplete_scores = []

    for line in lines:
        corrupted, score, st = is_corrupted_and_score(line)
        total_score += score
        if not corrupted:
            autocomplete_scores.append(autocomplete(line, st))
  
    print(total_score)
    print(sorted(autocomplete_scores)[len(autocomplete_scores)//2])
