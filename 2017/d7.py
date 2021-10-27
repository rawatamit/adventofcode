from collections import defaultdict
from itertools import groupby
from types import SimpleNamespace


class Node:
    def __init__(self, vid, wt, children) -> None:
        self.vid = vid
        self.wt = wt
        self.parent = None
        self.children = children
        self.total_wt = None
    
    def patch(self, nchild):
        for i, v in enumerate(self.children):
            self.children[i] = nchild[v]
            self.children[i].parent = self
    
    def total_weight(self):
        if self.total_wt is None:
            self.total_wt = self.wt
            for u in self.children:
                self.total_wt += u.total_weight()

        return self.total_wt
    
    def is_balanced(self):
        wt_map = defaultdict(list)
        for u in self.children:
            wt_map[u.total_weight()].append(u)
        return len(wt_map) == 1

    def __str__(self) -> str:
        schild = ''.join([str(x) for x in self.children])
        
        return (f'Node({self.v},{self.wt},{schild})'
                if self.children else f'Node({self.v},{self.wt})')


class Tree:
    def __init__(self) -> None:
        self.root = None
        self.vertices = {}
    
    def add_node(self, v, wt, children):
        node = Node(v, wt, children)
        self.vertices[v] = node

        if self.root is None:
            self.root = node
    
    def patch_up(self):
        for v in self.vertices.values():
            v.patch(self.vertices)
        
        for v in self.vertices.values():
            if v.parent is None:
                self.root = v
                break
    
    def balance_down(self, imbalance, node):
        # find weight of children
        wt_map = defaultdict(list)
        for u in node.children:
            wt_map[u.total_weight()].append(u)
        
        # no child is imbalanced, this node must be balanced
        if len(wt_map) == 1:
            return node.wt - imbalance
        
        group1 = None
        groupOther = None
        for k, v in wt_map.items():
            if len(v) == 1:
                group1 = (k, v[0])
            else:
                groupOther = (k, v)

        return self.balance_down(group1[0] - groupOther[0], group1[1])

    def balance_weight(self):
        return self.balance_down(0, self.root)

    def __str__(self):
        return f'Tree({self.root})'
 

def main():
    T = Tree()
    with open('d7.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                a, b = line.split(')')
                node, wt = a.split('(')
                edges = ([x.strip() for x in b[3:].split(',')]
                        if b.startswith(' ->') else [])
                
                T.add_node(node.strip(), int(wt), edges)
    
    T.patch_up()

    # part 1
    print(T.root.vid)

    # part 2
    x = T.balance_weight()
    print(x)


main()
