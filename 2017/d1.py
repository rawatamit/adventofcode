def captcha_sum(x, fn=None):
    l = [int(d) for d in str(x)]
    return sum([l[i] for i in range(len(l)) if l[i] == l[fn(i, len(l))]])


def main():
    with open('d1.txt') as fin:
        num = int(fin.read().strip())
    
    # part 1
    print(captcha_sum(num, lambda i, n: (i + 1) % n))

    # part 2
    print(captcha_sum(num, lambda i, n: (i + (n // 2)) % n))

main()
