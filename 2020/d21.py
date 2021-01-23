import collections


def read_food(line):
    ingredients, allergens = line.split('(contains')
    return ({ingredient.strip()
            for ingredient in ingredients.split()},
            [allergen.strip()
            for allergen in allergens[:-1].split(',')])


def make_allergen_graph():
    return collections.defaultdict(list)


def update_allergen_graph(G, ingredients, allergens):
    for allergen in allergens:
        G[allergen].append(ingredients)


def solve_graph(G):
    nG = make_allergen_graph()
    for allergen, possible_ingredients in G.items():
        maybe = None
        for ingredients in possible_ingredients:
            if maybe:
                maybe = maybe & ingredients
            else:
                maybe = ingredients
        update_allergen_graph(nG, maybe, [allergen])
    return nG


def allergen_ingredients(G):
    maybe_allergen = set()
    for ingredients in G.values():
        maybe_allergen |= ingredients[0]
    return maybe_allergen


def not_allergen(all_ingredients, maybe_allergen):
    nallergen = []
    for ingredients in all_ingredients:
        nallergen.extend(set(ingredients) - maybe_allergen )
    return nallergen


def solve_part2(G):
    # be careful, Q should not be a list
    # things should be added at the end
    # and removed at the front, otherwise
    # there can be an infinte loop where
    # we try to upate the same pair
    Q = collections.deque()
    mapping = {}
    for k, v in G.items():
        if len(v[0]) == 1:
            ingredient = v[0].pop()
            mapping[ingredient] = k
        else:
            Q.append((k, v[0]))
    
    while Q:
        allergen, ingredients = Q.popleft()
        if len(ingredients) == 1:
            ingredient = ingredients.pop()
            mapping[ingredient] = allergen
        else:
            updated_ingredients = set()
            for ingredient in ingredients:
                if ingredient not in mapping:
                    updated_ingredients.add(ingredient)
            Q.append((allergen, updated_ingredients))
    return mapping


if __name__ == '__main__':
    with open('d21.txt') as fin:
        G = make_allergen_graph()
        all_ingredients = []
        for line in fin:
            line = line.strip()
            ingredients, allergens = read_food(line)
            all_ingredients.append(ingredients)
            update_allergen_graph(G, ingredients, allergens)
        nG = solve_graph(G)

        # solution part 2
        mapping = solve_part2(nG)
        singrediets = sorted(mapping.items(), key=lambda x: x[1])
        canonical = ','.join([x[0] for x in singrediets])
        print(canonical)

        # solution part 1
        # maybe_allergen = allergen_ingredients(nG)
        # nallergen = not_allergen(all_ingredients, maybe_allergen)
        # print(len(nallergen))
