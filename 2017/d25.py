from collections import defaultdict


class State:
    def __init__(self, sid, actions) -> None:
        self.sid = sid
        self.actions = actions
    
    def __str__(self) -> str:
        return f'State({self.sid}, {self.actions})'
    
    def write(self, value):
        return self.actions[value]['write']

    def move_to(self, value):
        return self.actions[value]['move_to']
 
    def next_state(self, value):
        return self.actions[value]['next_state']


class TM:
    def __init__(self, begin_state) -> None:
        self.state = begin_state
        self.cursor = 0
        self.tape = defaultdict(int)
        self.statemap = {}
    
    def add_state(self, state):
        self.statemap[state.sid] = state
    
    def run(self, steps=1):
        for _ in range(steps):
            state = self.statemap[self.state]
            curvalue = self.tape[self.cursor]

            self.tape[self.cursor] = state.write(curvalue)
            self.cursor += state.move_to(curvalue)
            self.state = state.next_state(curvalue)
    
    def diagnostic_check(self):
        return sum(x for x in self.tape.values())


def run_test():
    stateA = State('A',
        {0: {'write': 1, 'move_to': +1, 'next_state': 'B'},
         1: {'write': 0, 'move_to': -1, 'next_state': 'B'}})
    
    stateB = State('B',
        {0: {'write': 1, 'move_to': -1, 'next_state': 'A'},
         1: {'write': 1, 'move_to': +1, 'next_state': 'A'}})
    
    tm = TM('A')
    tm.add_state(stateA)
    tm.add_state(stateB)

    tm.run(6)
    assert tm.diagnostic_check() == 3


def read_state(fin):
    sid = fin.readline().split()[-1][:-1]
    actions = {}

    for i in range(2):
        # skip the current value
        cval = fin.readline()
        write = fin.readline()[-3]
        move_to = +1 if fin.readline().endswith('right.\n') else -1
        next_state = fin.readline()[-3]
        actions[i] = {'write': int(write), 'move_to': move_to,
                      'next_state': next_state}
    
    return State(sid, actions)


def main():
    run_test()

    with open('d25.txt') as fin:
        begin = fin.readline()[-3]
        steps = int(fin.readline().split()[-2])
        # skip empty line
        fin.readline()

        tm = TM(begin)
        while True:
            state = read_state(fin)
            tm.add_state(state)
            if fin.readline() == '': break
    
    tm.run(steps)
    print(tm.diagnostic_check())


main()
