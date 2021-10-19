def next_index(index, l):
    return index % len(l)


def find_repeat2(banks, left=0, next=-1, steps=0, seen={}):
    while True:
        if left == 0:
            # check if we've already seen this config
            if tuple(banks) in seen:
                print(banks, steps, seen[tuple(banks)])
                return

            seen[tuple(banks)] = steps
            
            # if not, start redistributing again
            maxi = -1
            maxn = -1
            for i, x in enumerate(banks):
                if x > maxn:
                    maxn = x
                    maxi = i
            
            redis = banks[maxi]
            banks[maxi] = 0
            left, next, steps = redis, next_index(maxi+1, banks), steps + 1
        else:
            banks[next] += 1
            left, next = left - 1, next_index(next+1, banks)


def main():
    with open('d6.txt') as fin:
        banks = [int(x) for x in fin.read().strip().split()]

    # part 1 and 2
    # for part 2 subtract the time when the configuration is seen
    # again from the first time it was seen
    find_repeat2(banks)

main()
