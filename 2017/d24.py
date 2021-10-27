from collections import defaultdict


class Component:
    def __init__(self, a, b) -> None:
        self.ports = (a, b)
    
    def __repr__(self) -> str:
        return str(self)
    
    def __str__(self) -> str:
        return f'Component{self.ports}'
    
    @property
    def strength(self):
        return self.ports[0] + self.ports[1]
    
    def fits(self, port):
        return port in self.ports
    
    def opposite(self, port):
        return self.ports[0] if port == self.ports[1] else self.ports[1]


def build_bridges(components, bridge, port, used):
    next = filter(lambda it: not used[it] and it.fits(port), components)

    for component in next:
        used[component] = True
        nbridge = bridge + [component]
        yield nbridge
        yield from build_bridges(components, nbridge, component.opposite(port), used)
        used[component] = False


def part12(components):
    used = defaultdict(bool)
    bridges = build_bridges(components, [], 0, used)

    max_st = 0
    lens_and_strength = []

    for bridge in bridges:
        strength = sum(x.strength for x in bridge)
        max_st = max(max_st, strength)
        lens_and_strength.append((len(bridge), strength))

    max_st_longest = sorted(lens_and_strength, reverse=True)
    return max_st, max_st_longest[0]


def main():
    components = []
    with open('d24.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                components.append(Component(*(int(x) for x in line.split('/'))))

    max_strength, max_strength_longest = part12(components)
    print(max_strength, max_strength_longest)


main()
