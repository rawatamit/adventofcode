from aocd import get_data

def isinc(report):
    for i in range(1, len(report)):
        if report[i] <= report[i-1]:
            return False
    return True

def isdec(report):
    for i in range(1, len(report)):
        if report[i] >= report[i-1]:
            return False
    return True

def isdiff(report):
    for i in range(1, len(report)):
        diff = abs(report[i] - report[i-1])
        if diff > 3 or diff < 1:
            return False
    return True

def issafe(report):
    return (isinc(report) or isdec(report)) and isdiff(report)

def dampener(report, i=0):
    if issafe(report):
        return True

    for i in range(len(report)):
        treport = report[:i]+report[i+1:]
        if issafe(treport):
            return True
    return False

if __name__ == '__main__':
    data = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
    data = get_data(year=2024, day=2)
    nsafe = 0
    for line in data.split('\n'):
        report = [int(x) for x in line.split()]
        if issafe(report):
            nsafe += 1

    print('part1', nsafe)

    nsafe = 0
    for line in data.split('\n'):
        report = [int(x) for x in line.split()]
        if dampener(report):
            nsafe += 1

    print('part2', nsafe)

