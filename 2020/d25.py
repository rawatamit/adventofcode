def secret_loop_size(pubkey, subject_num=7):
    x = 1
    nloop = 0
    while x != pubkey:
        x = (x * subject_num) % 20201227
        nloop += 1
    return nloop


def transform_num(subject_num, times=1):
    x = 1
    for _ in range(times):
        x = (x * subject_num) % 20201227
    return x


if __name__ == '__main__':
    with open('d25.txt') as fin:
        card_pubkey = int(fin.readline().strip())
        door_pubkey = int(fin.readline().strip())

        card_loop_size = secret_loop_size(card_pubkey)
        #door_loop_size = secret_loop_size(door_pubkey)

        encrypt_key = transform_num(door_pubkey, card_loop_size)

        print(encrypt_key)
