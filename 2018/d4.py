from datetime import date, datetime, timedelta
from collections import defaultdict


def parse_timestamp(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M")


def parse_record_entry(s):
    timestamp, log = s.split('] ')
    return parse_timestamp(timestamp[1:]), log


def parse_guard_id(s):
    return int(s.split('Guard #')[1].split()[0])


def asleep_minutes(log):
    cur_guard = -1
    start_asleep = None
    asleep = defaultdict(list)

    for timestamp, entry in log:
        if entry.startswith('Guard'):
            cur_guard = parse_guard_id(entry)
        elif entry.startswith('falls'):
            start_asleep = timestamp
        else:
            delta = timestamp - start_asleep
            mins_asleep = range(start_asleep.minute, timestamp.minute)
            asleep[cur_guard].append((mins_asleep, delta.total_seconds() // 60))
    
    return asleep


def part1(log):
    guard_id = None
    guard_minute = None
    guard_asleep = -float('inf')
    asleep = asleep_minutes(sorted(log))

    for gid, info in asleep.items():
        total_asleep = 0
        minutes = [0 for _ in range(61)]
        for r, delta in info:
            # frequency of minutes asleep
            for x in r:
                minutes[x] += 1
            total_asleep += delta
        
        gminute = -1
        gval = -1
        for i, v in enumerate(minutes):
            if v > gval:
                gminute = i
                gval = v

        if guard_asleep < total_asleep:
            guard_id = gid
            guard_minute = gminute
            guard_asleep = total_asleep
    
    return guard_id * guard_minute


def part2(log):
    guard_id = None
    guard_minute = None
    guard_minute_times = -1
    asleep = asleep_minutes(sorted(log))

    for gid, info in asleep.items():
        minutes = [0 for _ in range(61)]
        for r, _ in info:
            # frequency of minutes asleep
            for x in r:
                minutes[x] += 1
        
        gminute = -1
        gtimes = -1
        for i, v in enumerate(minutes):
            if v > gtimes:
                gminute = i
                gtimes = v

        if guard_minute_times < gtimes:
            guard_id = gid
            guard_minute = gminute
            guard_minute_times = gtimes
    
    return guard_id * guard_minute


def main():
    log = []
    with open('d4.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                log.append(parse_record_entry(line))

    print(part1(log))
    print(part2(log))


main()
