import collections


def read_ticket(line):
    return [int(x) for x in line.split(',')]


def read_rule(line):
    desc, conditions = line.split(':')
    rules = conditions.split('or')

    ranges = []
    for rule in rules:
        begin, end = rule.split('-')
        ranges.append(range(int(begin), int(end)+1))
    return desc, ranges


def read_info(stream):
    # read rules
    line = stream.readline().strip()
    rules = []
    while line:
        rules.append(read_rule(line))
        line = stream.readline().strip()

    # read ticket
    # skip header
    line = stream.readline().strip()
    line = stream.readline().strip()
    my_ticket = read_ticket(line)

    # skip newline
    line = stream.readline().strip()

    # read nearby tickets
    # skip header
    line = stream.readline().strip()
    # first line of nearby tickets
    line = stream.readline().strip()
    nearby_tickets = []
    while line:
        tickets = read_ticket(line)
        nearby_tickets.append(tickets)
        line = stream.readline().strip()
    return rules, my_ticket, nearby_tickets


# solution part 1
def not_valid_for_any(rules, nearby_tickets):
    error_rate = 0
    for ticket in nearby_tickets:
        for num in ticket:
            valid = False
            for _, ranges in rules:
                for arange in ranges:
                    if num in arange:
                        valid = True
                        break
            if not valid:
                error_rate += num
    return error_rate


def is_valid_ticket(ticket, rules):
    def num_in_ranges(num, ranges):
        for arange in ranges:
            if num in arange:
                return True
        return False
    
    def num_in_one_range(num, rules):
        for _, ranges in rules:
            if num_in_ranges(num, ranges):
                return True
        return False
    
    for num in ticket:
        if not num_in_one_range(num, rules):
            return False
    
    return True


def find_valid_tickets(rules, nearby_tickets):
    valid_tickets = []
    for ticket in nearby_tickets:
        if is_valid_ticket(ticket, rules):
            valid_tickets.append(ticket)
    return valid_tickets


def check_ticket(ticket, index, ranges):
    for arange in ranges:
        if ticket[index] in arange:
            return True
    return False


def possible_positions(rule, my_ticket, tickets):
    unsolved_pos = range(len(my_ticket))
    field, ranges = rule
    positions = []

    for pos in unsolved_pos:
        valid_position = True
        # check if all tickets are valid for this field
        for ticket in tickets:
            if not check_ticket(ticket, pos, ranges):
                valid_position = False
                break
        # check my ticket
        if not check_ticket(my_ticket, pos, ranges):
            valid_position = False
        if valid_position:
            positions.append(pos)

    return positions


def solve_part2(rules, my_ticket, tickets):
    # be careful, Q should not be a list
    # things should be added at the end
    # and removed at the front, otherwise
    # there can be an infinte loop where
    # we try to upate the same pair
    Q = collections.deque()
    mapping = {}

    for rule in rules:
        desc, ranges = rule
        positions = possible_positions(rule, my_ticket, tickets)

        if len(positions) == 1:
            mapping[positions[0]] = desc
        else:
            Q.append((desc, positions))

    while Q:
        desc, positions = Q.popleft()
        if len(positions) == 1:
            mapping[positions[0]] = desc
        else:
            updated_positions = []
            for position in positions:
                if position not in mapping:
                    updated_positions.append(position)
            Q.append((desc, updated_positions))
    return mapping


if __name__ == '__main__':
    with open('d16.txt') as fin:
        rules, my_ticket, nearby_tickets = read_info(fin)
    # print(rules, my_ticket)
    # print(nearby_tickets)

    # part 1
    # error_rate = not_valid_for_any(rules, nearby_tickets)
    # print(error_rate)

    # part 2
    # ticket = [741, 921, 331, 658, 564, 106, 86, 719, 687, 377, 628, 390, 827, 152, 184, 334, 177, 152, 325, 20]
    # print(is_valid_ticket(ticket, rules))
    tickets = find_valid_tickets(rules, nearby_tickets)
    mapping = solve_part2(rules, my_ticket, tickets)
    mtf = [my_ticket[x] for x in mapping if mapping[x].startswith('departure')]
    print(mapping, mtf)
    # print(len(tickets), len(nearby_tickets))
    # field_map = solve_rules(rules, my_ticket, tickets)
    # print(field_map)
