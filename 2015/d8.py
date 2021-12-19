from aocd.models import Puzzle


def encode(data):
    i = 0
    mem_count = 0
    encoded = []
    inside_string = False

    while i < len(data.strip()):
        if data[i] == '\\':
            mem_count += 1

            if data[i+1] == 'x':
                # skip xab
                encoded.append(f'\\\\x{data[i+2:i+4]}')
                i += 4
            else:
                encoded.append(f'\\\\\\{data[i+1]}')
                i += 2
        elif data[i] == '"':
            if not inside_string:
                encoded.append('"\\"')
                # we are inside string now
                inside_string = not inside_string
            else:
                encoded.append('\\""')
            i += 1
        else:
            mem_count += 1
            encoded.append(data[i])
            i += 1
    
    return mem_count, ''.join(encoded)


if __name__ == '__main__':
    puzzle = Puzzle(year=2015, day=8)
    data = puzzle.input_data

    total_mem = 0
    total_chars = 0

    for s in data.split('\n'):
        mem_count, encoded = encode(s)

        total_mem += len(s) - mem_count
        total_chars += len(encoded) - len(s)
    
    print(total_mem, total_chars)
