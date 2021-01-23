import copy


def to_binary(num, digits):
    bits = [0] * digits
    mask = 0x1
    for i in range(digits):
        cmask = mask << i
        if (cmask & num) == cmask:
            bits[i] = 1
    return bits[::-1]


def apply_mask(memory, addr, mask, value, digits):
    bits = to_binary(value, digits)
    masked_bits = copy.deepcopy(bits)
    for i in range(digits):
        if mask[i] != 'X':
            masked_bits[i] = int(mask[i])
    memory[addr] = masked_bits
    return masked_bits


def to_int(v):
    value = 0
    for i in range(len(v)):
        # LSB is at the end, not beginning
        index = len(v) - 1 - i
        value += int(v[i]) * (2 ** index)
    return value


def iterate_all(s):
    Q = set([s])
    vs = set()
    while Q:
        v = Q.pop()
        X_in_v = False
        
        for i in range(len(v)):
            if v[i] == 'X':
                Q.add('{}1{}'.format(v[:i], v[i+1:]))
                Q.add('{}0{}'.format(v[:i], v[i+1:]))
                X_in_v = True

        if not X_in_v:
            vs.add(v)
    return vs


def apply_mask_part2(memory, addr, mask, value, digits):
    addr_mask = to_binary(addr, digits)
    for i in range(digits):
        if mask[i] == '1':
            addr_mask[i] = 1
        elif mask[i] == 'X':
            addr_mask[i] = 'X'

    addr_mask_str = ''.join(map(str, addr_mask))

    for mem_addr in iterate_all(addr_mask_str):
        dec_mem_addr = to_int(mem_addr)
        memory[dec_mem_addr] = value


def init_instructions(stream, init_fn=apply_mask):
    digits = 36
    mask = ' ' * digits
    memory = {}
    for line in stream:
        line = line.strip()
        if line.startswith('mask'):
            mask = line.split('=')[1].strip()
        else:
            mem, value = line.split('=')
            addr = int(mem.split('[')[1].strip()[:-1])
            init_fn(memory, addr, mask, int(value), digits)
    return memory


def sum_values_in_memory(memory):
    total_sum = 0
    for v in memory.values():
        total_sum += v # for first mask, this is to_int(v)
    return total_sum
 

if __name__ == "__main__":
    with open('d14.txt') as fin:
        memory = init_instructions(fin, apply_mask_part2)
    # print(memory)
    sum = sum_values_in_memory(memory)
    print(sum)
