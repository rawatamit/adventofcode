def checksum1(sheet):
    return sum(max(row) - min(row) for row in sheet)


def checksum2(sheet):
    csum = 0
    for row in sheet:
        for i, a in enumerate(row):
            for j, b in enumerate(row):
                if i != j and a % b == 0:
                    csum += a // b
    return csum


def main():
    sheet = []
    with open('d2.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                row = [int(x) for x in line.split()]
                sheet.append(row)

    # part 1
    print(checksum1(sheet))

    # part 2
    print(checksum2(sheet))


main()
