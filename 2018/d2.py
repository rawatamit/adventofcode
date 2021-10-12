def exactly_repeat(s, n):
    # returns True if there is a letter in s
    # that repeats exactly n times
    for c in s:
        if s.count(c) == n:
            return True
    return False


def differ_by(sa, sb):
    assert len(sa) == len(sb)
    count = 0
    for i, c in enumerate(sa):
        if c != sb[i]:
            count += 1
    return count


def main():
    with open('d2.txt') as fin:
        box_ids = [x for x in fin.read().split()]
    
    # part 1
    two_set = set()
    three_set = set()
    for box_id in box_ids:
        if exactly_repeat(box_id, 2):
            two_set.add(box_id)
        if exactly_repeat(box_id, 3):
            three_set.add(box_id)
    
    print(len(two_set) * len(three_set))

    # part 2
    for sa in box_ids:
        for sb in box_ids:
            if differ_by(sa, sb) == 1:
                print(''.join([c for i,c in enumerate(sa) if c == sb[i]]))
                return

main()
