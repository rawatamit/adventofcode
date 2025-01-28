from aocd import get_data


if __name__ == '__main__':
    data = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
    data = 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'
    data = get_data(year=2022, day=6)

    # part 1
    marker_len = 4
    for i in range(len(data) - marker_len + 1):
        if len(set(data[i:i+marker_len])) == marker_len:
            print(i + marker_len)
            break

    # part 2
    msg_len = 14
    for i in range(len(data) - msg_len + 1):
        if len(set(data[i:i+msg_len])) == msg_len:
            print(i + msg_len)
            break

