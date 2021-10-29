def scanner_location(ps, scan_range):
    to_init = (scan_range * 2) - 2
    return ps % to_init


def simulate_packet_move(firewall, start_ps, end_ps, all_moves=True):
    depth = 0 # also position of packet
    hits = []

    for ps in range(start_ps, end_ps + 1):
        scan_range = firewall.get(depth, -1)
        if scan_range != -1 and scanner_location(ps, scan_range) == 0:
            hits.append((ps, depth, scan_range))
            if not all_moves: break
        depth += 1
    
    return hits


def part1(firewall):
    max_ps = max(k for k in firewall.keys())
    hits = simulate_packet_move(firewall, 0, max_ps)
    total_severity = 0

    for ps, depth, scan_range in hits:
        total_severity += depth * scan_range
    
    return total_severity


def part2(firewall):
    max_ps = max(k for k in firewall.keys())
    cur_ps = 0

    while True:
        hits = simulate_packet_move(firewall, cur_ps, cur_ps + max_ps, all_moves=False)
        if not hits:
            return cur_ps
        cur_ps += 1


def main():
    with open('d13.txt') as fin:
        contents = fin.read().strip().split('\n')
        firewall = dict(map(lambda x: [int(y) for y in x.split(':')], contents))
    
    # part 1
    x = part1(firewall)
    print(x)

    x = part2(firewall)
    print(x)


main()
