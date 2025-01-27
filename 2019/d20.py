from aocd import get_data
import collections


def is_valid(G, r, c):
    rows = len(G)
    cols = len(G[0])
    if r < 0 or r >= rows:
        return False
    if c < 0 or c >= cols:
        return False
    return True


def neighbors(G, r, c):
    dr = [-1, 0, 0, 1]
    dc = [0, -1, 1, 0]
    ret = []

    for i in range(len(dr)):
        nr = r + dr[i]
        nc = c + dc[i]
        if is_valid(G, nr, nc):
            ret.append((nr, nc))

    return ret

# second character of portal opening
def second_char(G, r, c):
    dr = [0, 1]
    dc = [1, 0]
    br, bc = -1, -1

    # portal names are left to right, or top and down
    for i in range(len(dr)):
        nr = r + dr[i]
        nc = c + dc[i]
        if is_valid(G, nr, nc) and G[nr][nc].isupper():
            br, bc = nr, nc
            break
    return br, bc


def portal_opening(G, r, c):
    pr, pc = -1, -1
    for nr, nc in neighbors(G, r, c):
        if G[nr][nc] == '.':
            pr, pc = nr, nc
            break
    return pr, pc


def portal_name(a, b):
    return ''.join((a, b))


def get_portals(G):
    outer_rows = (2, len(G)-3)
    outer_cols = (2, len(G[0])-3)

    portal_levels = {}
    portals = collections.defaultdict(list)
    for r, row in enumerate(G):
        for c, cell in enumerate(row):
            # portal
            if cell.isupper():
                a = cell
                # get second character for this portal
                br, bc = second_char(G, r, c)
                if br < 0: continue
                b = G[br][bc]
                # get portal opening, as portal openings can be next to first
                # character or second character, try both locations. This skips
                # doing one ahead lookup.
                pr, pc = portal_opening(G, r, c)
                if pr < 0:
                    pr, pc = portal_opening(G, br, bc)

                assert pr >= 0 and pc >= 0
                # if there is an opening, add to map
                key = portal_name(a, b)
                portals[key].append((pr, pc))
                if (pr in outer_rows) or (pc in outer_cols):
                    portal_levels[(pr, pc)] = 'O'
                else:
                    portal_levels[(pr, pc)] = 'I'

    return portals, portal_levels


def search(G, start, end, portals, portal_ends):
    sr, sc = start

    Q = collections.deque()
    Q.append((sr, sc, 0))

    seen = set()
    seen.add((sr, sc))

    while Q:
        r, c, steps = Q.popleft()

        # reached the end
        if (r, c) == end:
            return steps

        next_cells = []

        # take a portal?
        portal_name = portal_ends.get((r, c), None)
        if portal_name not in (None, 'AA', 'ZZ'):
            # choose the opposite end of portal
            exits = portals[portal_name]
            for er, ec in exits:
                if (er, ec) != (r, c) and (er, ec) not in seen:
                    next_cells.append((er, ec))

        for nr, nc in neighbors(G, r, c):
            # skip non reachable spaces
            if G[nr][nc] == ' ' or G[nr][nc] == '#':
                continue
            if (nr, nc) in seen:
                continue
            # empty space 
            next_cells.append((nr, nc))

        # add all next cells to queue
        for nr, nc in next_cells:
            seen.add((nr, nc))
            Q.append((nr, nc, steps+1))

    return -1


def search2(G, start, end, portals, portal_ends, portal_levels):
    sr, sc = start

    # coordinates, recursion depth, and number of steps
    Q = collections.deque()
    Q.append((sr, sc, 0, 0))

    # coordinates and recursion depth
    seen = set()
    seen.add((sr, sc, 0))

    while Q:
        r, c, depth, steps = Q.popleft()

        # reached the end, with correct level
        if (r, c) == end:
            return steps

        next_cells = []

        # take a portal?
        portal_name = portal_ends.get((r, c), None)
        if portal_name not in (None, 'AA', 'ZZ'):
            # choose the opposite end of portal
            exits = portals[portal_name]
            for er, ec in exits:
                if (er, ec) != (r, c):
                    next_cells.append((er, ec))

        for nr, nc in neighbors(G, r, c):
            # skip non reachable spaces
            if G[nr][nc] == ' ' or G[nr][nc] == '#':
                continue
            # empty space
            next_cells.append((nr, nc))

        for nr, nc in next_cells:
            # level is inner or outer identification for a portal end
            old_level = portal_levels.get((r, c), 'Z')

            # skip all walled locations
            # from depth 0, outer level tiles are unreachable
            if depth == 0 and (r, c) != start and (nr, nc) != end and old_level == 'O':
                continue

            # at any depth > 0, AA and ZZ behave as a wall
            if depth > 0 and (nr, nc) in (start, end):
                continue

            # depth only changes for portal ends
            new_depth = depth
            if (nr, nc) in portal_levels:
                if old_level == 'I':
                    new_depth += 1
                elif old_level == 'O':
                    new_depth -= 1

            # skip if seen
            if (nr, nc, new_depth) in seen:
                continue

            seen.add((nr, nc, new_depth))
            Q.append((nr, nc, new_depth, steps+1))

    return -1


if __name__ == '__main__':
    example1 = """         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """

    example2 = """             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """

    data = example2
    data = get_data(year=2019, day=20)
    G = data.split('\n')

    portals, portal_levels = get_portals(G)
    portal_ends = {}
    for name, ends in portals.items():
        for end in ends:
            portal_ends[end] = name

    start = portals['AA'][0]
    end = portals['ZZ'][0]
    steps = search(G, start, end, portals, portal_ends)
    print('part1', steps)

    steps = search2(G, start, end, portals, portal_ends, portal_levels)
    print('part2', steps)

