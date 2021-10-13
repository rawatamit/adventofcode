class Node:
    def __init__(self, metadata, children) -> None:
        self.metadata = metadata
        self.children = children
    
    def __str__(self):
        schildren = [str(child) for child in self.children]
        return f'Node(metadata={self.metadata}, children={schildren})'


def make_tree(it):
    num_child = next(it)
    metadata_count = next(it)
    children = []

    for _ in range(num_child):
        child = make_tree(it)
        children.append(child)
    
    metadata = [next(it) for _ in range(metadata_count)]
    return Node(metadata, children)


def metadata_sum(node):
    children_sum = sum(metadata_sum(child) for child in node.children)
    return sum(node.metadata) + children_sum


def node_value(node):
    if len(node.children) == 0:
        return sum(node.metadata)
    else:
        value = 0
        for i in node.metadata:
            # treat i as child index
            child_index = i - 1
            if child_index < len(node.children):
                value += node_value(node.children[child_index])
        return value


def main():
    with open('d8.txt') as fin:
        tree = [int(x) for x in fin.read().split()]

    root = make_tree(iter(tree))
    
    # part 1
    print(metadata_sum(root))

    # part 2
    print(node_value(root))

main()
