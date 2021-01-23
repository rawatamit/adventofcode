def waittime(time_can_depart, busid):
    nticks_before = time_can_depart//busid
    time_after = nticks_before * busid + busid
    return time_after - time_can_depart


def min_waitime(time_can_depart, busids):
    return min((waittime(time_can_depart, busid), busid)
                for busid in busids)


if __name__ == "__main__":
    with open('d13.txt') as fin:
        time_can_depart = int(fin.readline())
        busids = [int(busid)
            for busid in fin.readline().strip().split(',')
            if busid != 'x']
    
    v = min_waitime(time_can_depart, busids)
    print(v)
