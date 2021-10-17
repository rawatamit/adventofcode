from collections import Counter


def valid_passphrases1(passphrases):
    valid = 0

    for passphrase in passphrases:
        c = Counter(passphrase)
        cm = c.most_common(1)
        if cm[0][1] == 1:
            valid += 1
    
    return valid


def valid_passphrases2(passphrases):
    valid = 0

    for passphrase in passphrases:
        l = sorted([''.join(sorted(list(x))) for x in passphrase])
        
        c = Counter(l)
        cm = c.most_common(1)
        if cm[0][1] == 1:
            valid += 1
    
    return valid


def main():
    passphrases = []
    with open('d4.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                passphrase = [x.strip() for x in line.split()]
                passphrases.append(passphrase)
    
    # part 1
    print(valid_passphrases1(passphrases))

    # part 2
    print(valid_passphrases2(passphrases))

main()
