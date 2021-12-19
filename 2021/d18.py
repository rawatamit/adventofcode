from aocd.models import Puzzle
import itertools
import math
import json


class Node:
    def __init__(self, parent, lhs=None, rhs=None) -> None:
        self.parent = parent
        self.lhs = lhs
        self.rhs = rhs
    
    def set_left(self, lhs):
        self.lhs = lhs

    def set_right(self, rhs):
        self.rhs = rhs
    
    def __str__(self) -> str:
        return f'({self.lhs}, {self.rhs})'


class Leaf:
    def __init__(self, parent, val) -> None:
        self.parent = parent
        self.val = val
    
    def __str__(self) -> str:
        return f'{self.val}'
    
    def set_value(self, val):
        self.val = val


def make_tree(l, parent=None):
    if isinstance(l, int):
        return Leaf(parent, l)
    else:
        curnode = Node(parent)
        curnode.set_left(make_tree(l[0], curnode))
        curnode.set_right(make_tree(l[1], curnode))
        return curnode


def inorder(root):
    if isinstance(root, Leaf):
        yield root
    else:
        yield from inorder(root.lhs)
        yield from inorder(root.rhs)


def find_pred(node, order):
    try:
        idx = order.index(node)
        if 0 < idx < len(order):
            return order[idx - 1]
    except (ValueError, IndexError):
        return None


def find_succ(node, order):
    try:
        idx = order.index(node)
        if 0 <= idx < len(order) - 1:
            return order[idx + 1]
    except (ValueError, IndexError):
        return None


def can_explode(node, depth=0):
    if isinstance(node, Node):
        return (depth == 4 or
                can_explode(node.lhs, depth + 1) or
                can_explode(node.rhs, depth + 1))
    return False


def can_split(node):
    if isinstance(node, Leaf):
        return node.val >= 10
    return can_split(node.lhs) or can_split(node.rhs)


def explode(node, order, depth=0):
    if isinstance(node, Node):
        if depth == 4:
            pred = find_pred(node.lhs, order)
            succ = find_succ(node.rhs, order)

            if pred is not None:
                pred.set_value(node.lhs.val + pred.val)

            if succ is not None:
                succ.set_value(node.rhs.val + succ.val)
            
            return True, Leaf(node.parent, 0)
        else:
            lhs_change, node.lhs = explode(node.lhs, order, depth + 1)
            if lhs_change: return True, node
            
            rhs_change, node.rhs = explode(node.rhs, order, depth + 1)
            if rhs_change: return True, node
    return False, node


def split(node):
    if isinstance(node, Leaf) and node.val >= 10:
        a = math.floor(node.val / 2)
        b = math.ceil(node.val / 2)
        newnode = Node(node.parent)
        newnode.lhs = Leaf(newnode, a)
        newnode.rhs = Leaf(newnode, b)
        return True, newnode
    
    if isinstance(node, Node):
        lhs_change, node.lhs = split(node.lhs)
        if lhs_change: return True, node

        rhs_change, node.rhs = split(node.rhs)
        if rhs_change: return True, node
    return False, node


def reduce_all(root):
    res = True
    while res:
        res = False
        if can_explode(root):
            change, root = explode(root, list(inorder(root)))
            if change: res = True
        elif can_split(root):
            change, root = split(root)
            if change: res = True

    return root


def magnitude(root):
    if isinstance(root, Leaf):
        return root.val
    else:
        return 3 * magnitude(root.lhs) + 2 * magnitude(root.rhs)


def add_tree(ta, tb):
    newroot = Node(None, ta, tb)
    ta.parent = newroot
    tb.parent = newroot
    return newroot


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=18)
    
    data = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''

    data = puzzle.input_data
    root = None
    for line in data.split('\n'):
        tr = make_tree(json.loads(line.strip()))

        if root is None:
            root = tr
        else:
            root = add_tree(root, tr)
            root = reduce_all(root)

    print(magnitude(root))

    perms = itertools.permutations(data.split('\n'), 2)
    sums = []

    for sa, sb in perms:
        # ta and tb are modified during reduction
        # create new trees every time
        ta = make_tree(json.loads(sa))
        tb = make_tree(json.loads(sb))
        sums.append(magnitude(reduce_all(add_tree(ta, tb))))
        
        ta = make_tree(json.loads(sa))
        tb = make_tree(json.loads(sb))
        sums.append(magnitude(reduce_all(add_tree(tb, ta))))
    
    print(max(sums))
