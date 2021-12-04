class BingoBoard:
    def __init__(self) -> None:
        self.rows = []
        self.marked_nums = set()
        self.last_marked = None
    
    def __str__(self) -> str:
        return f'Board<{self.rows}, {self.marked_nums}>'
    
    def num_rows(self):
        return len(self.rows)
    
    def num_columns(self):
        return len(self.rows[0])

    def add_row(self, row):
        self.rows.append(row)
    
    def get_last_marked(self):
        return self.last_marked
    
    def get_rows(self):
        for row in self.rows:
            yield row
    
    def get_columns(self):
        for col in zip(*self.rows):
            yield col
    
    def get_diagonals(self):
        # diagonal has entries (0, 0), (1, 1) and so on
        yield [row[i] for i, row in enumerate(self.rows)]
        # diagonal has entries (0, last_col), (1, second_last_col) and so on
        yield [row[self.num_columns() - i - 1] for i, row in enumerate(self.rows)]
    
    def get_marked_from(self, nums):
        return list(filter(lambda x: x in self.marked_nums, nums))
    
    def is_bingo(self):
        # check rows
        for row in self.get_rows():
            if len(self.get_marked_from(row)) == len(row):
                return True
    
        # check cols
        for col in self.get_columns():
            if len(self.get_marked_from(col)) == len(col):
                return True
        
        return False
    
    def mark_number(self, num):
        for row in self.get_rows():
            if row.count(num) != 0:
                self.marked_nums.add(num)
                self.last_marked = num
                break
    
    def score(self):
        unmarked_sum = 0
        for row in self.get_rows():
            unmarked_sum += sum([x for x in row if x not in self.marked_nums])
        return unmarked_sum * self.last_marked


def play_bingo_one_round(num_draw, boards):
    for board in boards:
        board.mark_number(num_draw)
        if board.is_bingo(): return True, board
    
    return False, None


def play_bingo(nums_to_draw, boards):
    for num_draw in nums_to_draw:
        res, board = play_bingo_one_round(num_draw, boards)
        if res: return board.score()


def play_bingo_last_board(nums_to_draw, boards):
    candidates = boards[:]
    draw_index = 0

    while len(candidates) > 1:
        num_draw = nums_to_draw[draw_index]
        draw_index += 1
        bingoed = []
        for board in candidates:
            board.mark_number(num_draw)
            if board.is_bingo():
                bingoed.append(board)
        
        candidates = [board
                        for board in candidates
                        if board not in bingoed]

    board = candidates.pop()
    while not board.is_bingo():
        num_draw = nums_to_draw[draw_index]
        draw_index += 1
        board.mark_number(num_draw)
    
    return board.score()


def read_bingo_board(fin):
    board = BingoBoard()

    for _ in range(5):
        row = [int(x) for x in fin.readline().strip().split()]
        board.add_row(row)
     
    return board


if __name__ == '__main__':
    boards = []

    with open('d4.txt') as fin:
        nums_to_draw = [int(x) for x in fin.readline().split(',')]
        
        while True:
            if fin.readline() == '': break
            board = read_bingo_board(fin)
            boards.append(board)
    
    # Run part 1 and 2 separately, state of board is modified.
    # However, the side effects are such that it doesn't matter
    # if both parts are run at once.

    # part 1
    print(play_bingo(nums_to_draw, boards))

    # part 2
    print(play_bingo_last_board(nums_to_draw, boards))
