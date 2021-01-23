import copy


def read_grid(stream):
    return [[cell for cell in line.strip()]
            for line in stream.readlines()]


def grid_to_str(G):
    return '\n'.join(''.join(row) for row in G)


def neighbours(G, r, c):
    ns = [(-1, -1), (-1, 0), (-1, 1),
          ( 0, -1),          ( 0, 1),
          ( 1, -1), ( 1, 0), ( 1, 1)]
    valid_ns = []
    for dr, dc in ns:
        nr = r + dr
        nc = c + dc
        if nr >= 0 and nr < len(G) and nc >= 0 and nc < len(G[0]):
            valid_ns.append((nr, nc))
    return valid_ns


def occupied_neighbours(G, r, c):
    noccupied = 0
    for nr, nc in neighbours(G, r, c):
        if G[nr][nc] == '#':
            noccupied += 1
    return noccupied


def total_occupied(G):
    occupied = 0
    for r in range(len(G)):
        for c in range(len(G[0])):
            if G[r][c] == '#':
                occupied += 1
    return occupied


def one_iteration(G_orig):
    G = copy.deepcopy(G_orig)
    for r in range(len(G)):
        for c in range(len(G[0])):
            noccupied = occupied_neighbours(G_orig, r, c)
            if G_orig[r][c] == 'L' and noccupied == 0:
                G[r][c] = '#'
            if G_orig[r][c] == '#' and noccupied >= 4:
                G[r][c] = 'L'
    return G


def fixed_point(G):
    while True:
        G_new = one_iteration(G)
        break
        if G_new == G:
            return G_new
        else:
            G = G_new


def first_visible_neighbour_in_view(G, r, c):
    def is_valid(G, r, c):
        return r >= 0 and r < len(G) and c >= 0 and c < len(G[0])
    
    up = lambda r, c: (r - 1, c)
    down = lambda r, c: (r + 1, c)
    left = lambda r, c: (r, c - 1)
    right = lambda r, c: (r, c + 1)
    diag_up_left = lambda r, c: (r - 1, c - 1)
    diag_up_right = lambda r, c: (r - 1, c + 1)
    diag_down_left = lambda r, c: (r + 1, c - 1)
    diag_down_right = lambda r, c: (r + 1, c + 1)
    ns_fn = [up, down, left, right,
             diag_up_left, diag_up_right,
             diag_down_left, diag_down_right]
    ns = []
    for fn in ns_fn:
        nr, nc = fn(r, c)
        while is_valid(G, nr, nc):
            if G[nr][nc] != '.':
                ns.append((nr, nc))
                break
            nr, nc = fn(nr, nc)
    return ns


def occupied_neighbours_in_view(G, r, c):
    noccupied = 0
    for nr, nc in first_visible_neighbour_in_view(G, r, c):
        if G[nr][nc] == '#':
            noccupied += 1
    return noccupied


def one_iteration_in_view(G_orig):
    G = copy.deepcopy(G_orig)
    for r in range(len(G)):
        for c in range(len(G[0])):
            noccupied = occupied_neighbours_in_view(G_orig, r, c)
            if G_orig[r][c] == 'L' and noccupied == 0:
                G[r][c] = '#'
            if G_orig[r][c] == '#' and noccupied >= 5:
                G[r][c] = 'L'
    return G


def fixed_point_in_view(G):
    while True:
        G_new = one_iteration_in_view(G)
        if G_new == G:
            return G_new
        else:
            G = G_new


if __name__ == "__main__":
    with open('d11.txt') as fin:
        G = read_grid(fin)
    #G_fix = fixed_point(G)
    #print(total_occupied(G_fix))

    G_fix = fixed_point_in_view(G)
    print(total_occupied(G_fix))
