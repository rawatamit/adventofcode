from aocd import get_data
import collections


def is_correct_order(pages, G):
    for i, page in enumerate(pages):
        # all pages that should be after this page
        after = G.get(page, [])
        for j in range(0, i):
            if pages[j] in after:
                return False
    return True


def fix_order(pages, G):
    fix = pages[:]
    for i, page in enumerate(fix):
        # all pages that should be after this page
        after = G.get(page, [])
        for j in range(0, i):
            # swap these pages
            if fix[j] in after:
                fix[i], fix[j] = fix[j], fix[i]
    return fix


if __name__ == '__main__':
    data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
    data = get_data(year=2024, day=5)
    G = collections.defaultdict(list)

    part1 = 0
    part2 = 0
    for line in data.split('\n'):
        line = line.strip()
        if not line:
            continue
        if '|' in line:
            a, b = line.split('|')
            # b should come after a
            if a != b:
                G[int(a)].append(int(b))
        else:
            pages = [int(x) for x in line.split(',')]
            if is_correct_order(pages, G):
                part1 += pages[len(pages)//2]
            else:
                neworder = fix_order(pages, G)
                part2 += neworder[len(neworder)//2]

    print('part1', part1)
    print('part2', part2)
