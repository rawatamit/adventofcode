from collections import defaultdict
from functools import reduce
import re


class Bot:
    def __init__(self, bot_id) -> None:
        self.bot_id = bot_id
        self.chips = []
    
    def set_instruction(self, lo_recv, lo_recv_id, hi_recv, hi_recv_id):
        self.instruction = [lo_recv, lo_recv_id, hi_recv, hi_recv_id]
    
    def get_instruction(self):
        return self.instruction
    
    def add_chip(self, chip_id):
        self.chips.append(chip_id)
    
    def num_chips(self):
        return len(self.chips)
    
    def min_chip(self):
        chip_id = min(self.chips)
        self.chips.remove(chip_id)
        return chip_id

    def max_chip(self):
        chip_id = max(self.chips)
        self.chips.remove(chip_id)
        return chip_id


def add_bot(bots, bot_id):
    if bot_id not in bots:
        bots[bot_id] = Bot(bot_id)
    return bots[bot_id]


if __name__ == '__main__':
    bots = {}
    bins = defaultdict(list)

    with open('d10.txt') as fin:
        instructions = fin.read().split('\n')

        # allocate chips to bots
        bot_chip_re = r'value (\d+) goes to bot (\d+)'

        # now start moving chips
        bot_move_chip_re = r'bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)'

        for line in instructions:
            if bot_chip := re.search(bot_chip_re, line):
                chip_id = int(bot_chip.group(1))
                bot_id = int(bot_chip.group(2))

                bot = add_bot(bots, bot_id)
                bot.add_chip(chip_id)
            elif bot_move_chip := re.search(bot_move_chip_re, line):
                bot_id = int(bot_move_chip.group(1))
                lo_recv = bot_move_chip.group(2)
                lo_recv_id = int(bot_move_chip.group(3))
                hi_recv = bot_move_chip.group(4)
                hi_recv_id = int(bot_move_chip.group(5))

                bot = add_bot(bots, bot_id)
                bot.set_instruction(lo_recv, lo_recv_id, hi_recv, hi_recv_id)

    # run instructions on valid bots
    Q = [bot for bot in bots.values() if bot.num_chips() >= 2]

    while Q:
        bot = Q.pop()
        lo_recv, lo_recv_id, hi_recv, hi_recv_id = bot.get_instruction()

        lo_chip = bot.min_chip()
        hi_chip = bot.max_chip()

        if (17, 61) == (lo_chip, hi_chip):
            print(bot.bot_id)
 
        if lo_recv == 'output':
            bins[lo_recv_id].append(lo_chip)
        else:
            bot = add_bot(bots, lo_recv_id)
            bot.add_chip(lo_chip)
            if bot.num_chips() >= 2: Q.append(bot)

        if hi_recv == 'output':
            bins[hi_recv_id].append(hi_chip)
        else:
            bot = add_bot(bots, hi_recv_id)
            bot.add_chip(hi_chip)
            if bot.num_chips() >= 2: Q.append(bot)

    res = reduce(lambda x, y: x * y, [bins[bin_id][0] for bin_id in (0, 1, 2)])
    print(res)
