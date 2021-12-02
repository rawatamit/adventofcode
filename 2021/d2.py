if __name__ == '__main__':
    forward = 0
    depth = 0

    with open('d2.txt') as fin:
        for line in fin:
            cmd, value = line.strip().split()
            value = int(value)
            if cmd == 'forward':
                forward += value
            elif cmd == 'down':
                depth += value
            elif cmd == 'up':
                depth -= value
    
    print(forward * depth)

    depth = 0
    forward = 0
    aim = 0

    with open('d2.txt') as fin:
        for line in fin:
            cmd, value = line.strip().split()
            value = int(value)
            if cmd == 'forward':
                forward += value
                depth += aim * value
            elif cmd == 'down':
                aim += value
            elif cmd == 'up':
                aim -= value
    
    print(forward * depth)
