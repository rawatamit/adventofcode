class Node:
    def __init__(self, val, next_node=None) -> None:
        self.val = val
        self.next = next_node
    
    def __str__(self) -> str:
        return f'Node({self.val})'


class CircularList:
    def __init__(self, init=[]) -> None:
        self.len = 0
        self.head = None
        self.tail = None
        self.curpos = None

        for x in init:
            self.insert_end(x)
    
    def move_by(self, step):
        assert self.curpos is not None

        for _ in range(step % self.len):
            self.curpos = self.curpos.next
    
    def insert_cur(self, x):
        if self.head is None:
            self.insert_end(x)
        else:
            node = Node(x, self.curpos.next)
            self.curpos.next = node
            self.curpos = node

        self.len += 1
    
    def insert_end(self, x):
        if self.head is None:
            node = Node(x)
            self.head = node
            self.tail = node
            self.curpos = node
            self.tail.next = self.head
        else:
            node = Node(x, self.tail.next)
            self.tail.next = node
            self.tail = node
        
        assert self.tail.next is self.head
        self.len += 1
    
    def find(self, x):
        tnode = self.head
        for _ in range(self.len):
            if tnode.val == x:
                return tnode
            tnode = tnode.next
    
    def __str__(self) -> str:
        l = []
        t = self.head

        for _ in range(self.len):
            l.append(str(t))
            t = t.next
        
        return ' -> '.join(l)


def part1(step, max_value, value):
    c = CircularList([0])
    for i in range(1, max_value+1):
        c.move_by(step)
        c.insert_cur(i)
    
    node_value = c.find(value)
    print(node_value, node_value.next)


def part2(step, max_value):
    len = 1
    curpos = 0
    after_one = None
    for x in range(1, max_value+1):
        curpos = ((curpos + step) % len) + 1
        if curpos == 1:
            after_one = x
        len += 1
    return after_one


def main():
    part1(348, 2017, 2017)

    x = part2(348, 50000000)
    print(x)


main()
