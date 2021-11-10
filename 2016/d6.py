from collections import Counter


if __name__ == '__main__':
    with open('d6.txt') as fin:
        repeats = fin.read().split('\n')
        counters = []
        for chars in zip(*repeats):
            counters.append(Counter(chars))
        
        message1 = []
        for pos_counter in counters:
            message1.append(pos_counter.most_common(n=1)[0][0])
        
        print(''.join(message1))

        message2 = []
        for pos_counter in counters:
            message2.append(pos_counter.most_common()[-1][0])
        
        print(''.join(message2))
