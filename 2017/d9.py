from io import StringIO


def groups_score_and_garbage(s):
    group_st = []
    count = 0
    cur_score = 0
    total_score = 0
    garbage_chars = 0
    garbage = False
    canceled = False

    for _, c in enumerate(s):
        if canceled:
            # only cancel one character after !
            canceled = False
        elif c == '!':
            # this is a ! character, cancel the next one
            canceled = True
        elif c == '>':
            assert garbage is True
            garbage = False
        elif garbage:
            # skip character inside garbage
            garbage_chars += 1
        elif c == '<':
            garbage = True
        elif c == '{':
            cur_score += 1
            group_st.append('{')
        elif c == '}':
            assert group_st.pop() == '{'
            total_score += cur_score
            cur_score -= 1
            count += 1

    return count, total_score, garbage_chars


def num_groups(s):
    groups, _, _ = groups_score_and_garbage(s)
    return groups


def num_score(s):
    _, score, _ = groups_score_and_garbage(s)
    return score


def num_garbage(s):
    _, _, garbage = groups_score_and_garbage(s)
    return garbage


def run_tests():
    assert num_groups('{}') == 1
    assert num_groups('{{{}}}') == 3
    assert num_groups('{{},{}}') == 3
    assert num_groups('{{{},{},{{}}}}') == 6
    assert num_groups('{<{},{},{{}}>}') == 1
    assert num_groups('{<a>,<a>,<a>,<a>}') == 1
    assert num_groups('{{<a>},{<a>},{<a>},{<a>}}') == 5
    assert num_groups('{{<!>},{<!>},{<!>},{<a>}}') == 2

    assert num_score('{}') == 1
    assert num_score('{{{}}}') == 6
    assert num_score('{{},{}}') == 5
    assert num_score('{{{},{},{{}}}}') == 16
    assert num_score('{<a>,<a>,<a>,<a>}') == 1
    assert num_score('{{<ab>},{<ab>},{<ab>},{<ab>}}') == 9
    assert num_score('{{<!!>},{<!!>},{<!!>},{<!!>}}') == 9
    assert num_score('{{<a!>},{<a!>},{<a!>},{<ab>}}') == 3

    assert num_garbage('<>') == 0
    assert num_garbage('<random characters>') == 17
    assert num_garbage('<<<<>') == 3
    assert num_garbage('<{!>}>') == 2
    assert num_garbage('<!!>') == 0
    assert num_garbage('<!!!>>') == 0
    assert num_garbage('<{o"i!a,<{i<a>') == 10


def main():
    with open('d9.txt') as fin:
        s = fin.read().strip()
    
    run_tests()

    # part 1
    print(num_score(s))

    # part 2
    print(num_garbage(s))

main()
