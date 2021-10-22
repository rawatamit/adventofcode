from collections import defaultdict


def dfs(u, G, visited, cc):
    visited[u] = cc

    for v in G[u]:
        if v not in visited:
            visited[v] = u
            dfs(v, G, visited, cc)


def explore(G):
    cc = 0
    visited = {}
    for u in G.keys():
        if u not in visited:
            dfs(u, G, visited, cc)
            cc += 1
    
    return visited


def ngroup0(visited):
    return sum([1 for u, cc in visited.items() if cc == visited[0]])


def total_groups(visited):
    return len({cc for cc in visited.values()})


def main():
    G = defaultdict(list)
    with open('d12.txt') as fin:
        for line in fin:
            if line.strip():
                v, ns = line.strip().split('<->')
                G[int(v)] = [int(x) for x in ns.split(',')]
    
    visited = explore(G)

    # part 1
    print(ngroup0(visited))

    # part 2
    print(total_groups(visited))


main()
