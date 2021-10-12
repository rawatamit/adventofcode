from itertools import cycle

def main():
    with open('d1.txt') as fin:
        nums = [int(x) for x in fin.read().split()]
    
    # part 1
    print(sum(nums))

    # part 2
    freq = 0
    seen = set([freq])
    for x in cycle(nums):
        freq += x

        if freq in seen:
            print(f'seen twice: {freq}')
            break
        
        seen.add(freq)

main()
