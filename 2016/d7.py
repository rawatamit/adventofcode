import re


def is_abba(s):
    return len(s) == 4 and s[0] != s[1] and s[:2] == s[:-3:-1]


def groups_of(s, n=1):
    i = 0
    while i+n <= len(s):
        yield s[i:i+n]
        i += 1


def ipv7(s):
    outers = []
    hnets = []

    for x in s.split('['):
        if ']' in x:
            hnet, outer = x.split(']')
            hnets.append(hnet)
            outers.append(outer)
        else:
            outers.append(x)

    return outers, hnets


def has_abba(s):
    return any(is_abba(g) for g in groups_of(s, 4))


def support_TLS(s):
    outers, hnets = ipv7(s)
    return (any(has_abba(outer) for outer in outers) and
            not any(has_abba(hnet) for hnet in hnets))


def is_aba(s):
    return len(s) == 3 and s[0] != s[1] and s[0] == s[-1]


def is_bab(s, aba):
    bab = aba[1] + aba[0] + aba[1]
    return s == bab


def support_SSL(s):
    outers, hnets = ipv7(s)

    abas = [g for outer in outers
              for g in groups_of(outer, 3)
              if is_aba(g)]
    
    for aba in abas:
        has_bab = any(is_bab(hnet_g, aba)
                      for hnet in hnets
                      for hnet_g in groups_of(hnet, 3))
        if has_bab: return True

    return False


if __name__ == '__main__':
    with open('d7.txt') as fin:
        addrs = fin.read().split('\n')
        count = sum(1 for addr in addrs if support_TLS(addr))
        print(count)

        count = sum(1 for addr in addrs if support_SSL(addr))
        print(count)
