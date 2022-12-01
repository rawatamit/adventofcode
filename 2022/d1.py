from aocd import get_data


if __name__ == '__main__':
    data = get_data(year=2022, day=1)
    cur_elf = 0
    max_elf = -1
    all_elf_cals = []

    for line in data.splitlines():
        cal = line.strip()
        if cal:
            cur_elf += int(cal)
        else:
            max_elf = max(max_elf, cur_elf)
            all_elf_cals.append(cur_elf)
            cur_elf = 0
    print(sum(sorted(all_elf_cals, reverse=True)[:3]))
