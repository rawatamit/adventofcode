from collections import deque

def find_all_bodies(u, G):
    ret = []
    while u in G:
        v = G[u]
        ret.append(v) 
        u = v
    return ret

def find_path_for_all_bodies(G):
    path_sum = 0
    for u in G.keys():
        path = find_all_bodies(u, G)
        path_sum += len(path)
    return path_sum

def part1_graph_read(filepath):
    G = {}
    with open(filepath) as fin:
        for line in fin:
            line = line.strip()
            if line:
                A, B = line.strip().split(')')
                G[B] = A # B orbits around A
    return G

def add_edge(u, v, G):
    if u in G:
        G[u].append(v)
    else:
        G[u] = [v]

# def part2_graph_read(filepath):
#     G = {}
#     with open(filepath) as fin:
#         for line in fin:
#             line = line.strip()
#             if line:
#                 A, B = line.strip().split(')')
#                 add_edge(A, B, G)
#                 add_edge(B, A, G)
#     return G

# def orbital_transfers(s, e, G):
#     Q = deque([(s, 0)])
#     parent = {s:None}
#     visited = set()
# 
#     while Q:
#         u, pl = Q.popleft()
#         if u == e: return pl - 2
# 
#         if u in visited: continue
#         visited.add(u)
# 
#         for v in G[u]:
#             if v not in visited:
#                 parent[v] = u
#                 Q.append((v, pl+1))
#     return -1

def orbital_transfers(s, e, G):
    # path to the central orbital body
    spath = find_all_bodies(s, G)
    epath = find_all_bodies(e, G)

    # find first intersection
    i, j = len(spath) - 1, len(epath) - 1
    while i >= 0 and j >= 0 and spath[i] == epath[j]:
        i -= 1
        j -= 1
    
    assert(spath[i+1] == epath[j+1])
    return i+1 + j+1


def main():
    # G = part1_graph_read('d6.txt')
    # path_sum = find_path_for_all_bodies(G)
    # print(path_sum)

    ## can be solved two ways
    # G = part2_graph_read('d6.txt')
    # transfers = orbital_transfers('YOU', 'SAN', G)
    G = part1_graph_read('d6.txt')
    transfers = orbital_transfers('YOU', 'SAN', G)
    print(transfers)

main()
