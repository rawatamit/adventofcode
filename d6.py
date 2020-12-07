def group_answers(stream):
    group = []
    for line in stream:
        line = line.strip()
        if line:
            group.append(line)
        else:
            yield group
            group = []
    
    yield group


def sum_counts1(stream):
    def answers(group):
        ans = set()
        for line in group:
            ans.update(line)
        return ans

    return sum([len(answers(group))
        for group in group_answers(stream)])


def sum_counts2(stream):
    def answers(group):
        ans = set(group[0])
        for line in group:
            ans = ans & set(line)
        return ans

    return sum([len(answers(group))
        for group in group_answers(stream)])


if __name__ == "__main__":
    with open('d6.txt') as fin:
        x = sum_counts2(fin)
        print(x)
