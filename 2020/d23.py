def print_cups(cups):
    cup = cups[1]
    while cup != 1:
        print(cup, end='')
        cup = cups[cup]
        print('\n' if cup == 1 else ', ', end='')


def find_destination_cup(current_cup, cups, lowest_val, highest_val):
    def update_label(cup):
        cup -= 1
        if cup < lowest_val:
            return highest_val
        else:
            return cup
    
    # if current_cup is already lowest_val
    # then we need to get the right value
    dest_cup = update_label(current_cup)
    while dest_cup in cups:
        dest_cup = update_label(dest_cup)
    return dest_cup


def make_move(cups, current_cup, lowest_val, highest_val):
    # three cups after current
    a = cups[current_cup]
    b = cups[a]
    c = cups[b]
    
    # destination cup
    dest_cup = \
        find_destination_cup(current_cup,
                             (a, b, c),
                             lowest_val, highest_val)

    # next cup to destination cup
    dest_next = cups[dest_cup]

    # next cup to current cup is destination cup
    cups[current_cup] = cups[c]

    # next cup after destination cup is
    # the first cup after current cup
    cups[dest_cup] = a

    # next cup after the third cup is the
    # next cup after destination cup
    cups[c] = dest_next
    return cups[current_cup]


def make_n_moves(cups, current_cup, nmoves, lowest_val, highest_val):
    for i in range(nmoves):
        current_cup = make_move(cups, current_cup, lowest_val, highest_val)


def make_cup_list(cups, highest_val, total_entries):
    icups = [0] * (total_entries + 1)

    for i in range(0, len(cups) - 1):
        icups[int(cups[i])] = int(cups[i+1])

    # disable for part 1
    icups[int(cups[-1])] = highest_val + 1
    for i in range(highest_val+1, total_entries):
        icups[i] = i + 1
    
    icups[total_entries] = int(cups[0])
 
    # enable for part 1
    # icups[int(cups[-1])] = int(cups[0])
    return icups


if __name__ == "__main__":
    # solution part 2
    lowest_val = 1
    highest_val = 9
    total_entries = 1000000
    nmoves = 10000000
    cups = make_cup_list('538914762', highest_val, total_entries)

    # print_cups(cups)
    # print([i for i in range(total_entries+1)])
    # print(cups)

    # highest value is total number of entries now
    # as all of the cups have been lined correctly
    make_n_moves(cups, 5, nmoves, lowest_val, total_entries)
    print(cups[1], cups[cups[1]])

    # solution part 1
    # lowest_val = 1
    # highest_val = 9
    # nmoves = 100
    # cups = make_cup_list('538914762', highest_val)
    # make_n_moves(cups, 5, nmoves, lowest_val, highest_val)
    # print_cups(cups)
