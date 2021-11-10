import hashlib


def five_zero_hash(s):
    i = 1
    while True:
        si = f'{s}{i}'.encode('utf-8')
        md5_hash = hashlib.md5(si).hexdigest()
        if md5_hash[:5] == '00000':
            yield si, md5_hash
        i += 1


def interesting_hash(s, n=1):
    i = 0
    passwd = []
    for _, md5_hash in five_zero_hash(s):
        passwd.append(md5_hash[5])
        i += 1
        if i == n: break
    return ''.join(passwd)


def interesting_hash2(s, length=1):
    passwd = [None for _ in range(length)]
    have = 0

    for _, md5_hash in five_zero_hash(s):
        index = -1
        index_str, value = md5_hash[5], md5_hash[6]

        if index_str.isdigit():
            index = int(index_str) if int(index_str) < len(passwd) else -1

        if index != -1 and passwd[index] is None:
            passwd[index] = value
            have += 1
            if have == len(passwd): break

    return ''.join(passwd)


if __name__ == '__main__':
    passwd = interesting_hash('abbhdwsy', 8)
    print(passwd)

    passwd = interesting_hash2('abbhdwsy', 8)
    print(passwd)
