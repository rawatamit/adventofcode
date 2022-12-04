from aocd import get_data


def item_priority(item):
    if item.islower():
        return ord(item) - ord('a') + 1
    else:
        return ord(item) - ord('A') + 27


if __name__ == '__main__':
    data = '''vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw '''
    data = get_data(year=2022, day=3)

    lines = [line.strip() for line in data.splitlines()]

    # part 1
    priority_sum = 0
    for line in lines:
        rsack1 = line[:len(line)//2]
        rsack2 = line[len(line)//2:]
        common = set(rsack1) & set(rsack2)
        priority_sum += sum(map(item_priority, common))
    print(priority_sum)

    # part 2
    priority_sum = 0
    for i in range(0, len(lines), 3):
        common = set(lines[i]) & set(lines[i + 1]) & set(lines[i + 2])
        priority_sum += sum(map(item_priority, common))
    print(priority_sum)
