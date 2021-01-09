def play_game(nums, nmoves):
    num_map = {}
    current_num = 0

    for turn in range(len(nums)-1):
        num_map[nums[turn]] = turn+1

    current_num = nums[-1]
    for turn in range(len(nums)+1, nmoves+1):
        last_turn = turn - 1
        if current_num in num_map:
            next_num = last_turn - num_map[current_num]
        else:
            next_num = 0
        num_map[current_num] = last_turn
        current_num = next_num

    return current_num


if __name__ == '__main__':
    nums = [0,3,6]
    num = play_game(nums, 2020)
    print(num)
