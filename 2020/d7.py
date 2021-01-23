def decompose_rule(rule):
    outer_bag, other = rule.split('bags contain', 1)
    if other.strip() == 'no other bags.':
        return outer_bag.strip(), []
    else:
        contained = other.split(',')
        edges = []
        for inner_bag in contained:
            num, desc = inner_bag.strip().split(' ', 1)
            color = desc.rsplit(' ', 1)[0]
            edges.append((int(num), color.strip()))
        return outer_bag.strip(), edges


def make_graph(stream):
    G = {}

    for rule in stream:
        rule = rule.strip()
        if rule:
            bag, edges = decompose_rule(rule)
            G[bag] = edges
    
    return G


def find_node(G, s, e):
    Q = [s]
    visited = {}
    while Q:
        u = Q.pop()
        visited[u] = True
        if u == e:
            return True
        else:
            for n, v in G[u]:
                if v not in visited:
                    Q.append(v)
    return False


def bags_contained(G, s, visited):
    if s in visited:
        return visited[s]
    
    count = 1
    for n, v in G[s]:
        count += n * bags_contained(G, v, visited)
    visited[s] = count
    return count


def find_shiny_gold(G):
    visited = {}
    e = 'shiny gold'
    count = 0
    for u in G.keys():
        if u not in visited and u != e:
            visited[u] = True
            ret = find_node(G, u, e)
            count += 1 if ret else 0
    return count


if __name__ == "__main__":
    with open('d7.txt') as fin:
        G = make_graph(fin)
        count = bags_contained(G, 'shiny gold', {})
        print(count -1)
