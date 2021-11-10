import collections
import functools
import string


def compare(a, b):
    char_a, freq_a = a
    char_b, freq_b = b
    if (freq_a > freq_b) or (freq_a == freq_b and char_a < char_b):
        return -1
    elif freq_a == freq_b and char_a == char_b:
        return 0
    else:
        return 1


def break_name(name):
    pieces = name.split('-')
    sector_id, checksum = pieces[-1].split('[')
    return pieces[:-1], int(sector_id), checksum[:-1]


def find_common(pieces):
    counter = collections.Counter()
    for piece in pieces:
        this_counter = collections.Counter(piece)
        counter.update(this_counter)
    
    sorted_letters = sorted(counter.items(), key=functools.cmp_to_key(compare))
    five_common = [x for x, _ in sorted_letters[:5]]
    return ''.join(five_common)


def shift_cipher(s, amount):
    table = string.ascii_lowercase
    decoded = []
    for c in s:
        index = (table.index(c) + amount) % len(table)
        decoded.append(table[index])
    return ''.join(decoded)


def decode_message(pieces, sector_id):
    return [shift_cipher(s, sector_id) for s in pieces]


def real_rooms(rooms):
    for name in rooms:
        pieces, sector_id, checksum = break_name(name)
        five_common = find_common(pieces)
        if five_common == checksum:
            yield pieces, sector_id


if __name__ == '__main__':
    with open('d4.txt') as fin:
        rooms = fin.read().split('\n')
        sum_id = 0
        for pieces, sid in real_rooms(rooms):
            sum_id += sid
        
            message = decode_message(pieces, sid)
            if 'northpole' in message:
                print(sid, message)
        
        print(sum_id)
