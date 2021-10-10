import math
from collections import defaultdict


class Recipe:
    def __init__(self, element, quantity, constituents):
        self.element = element
        self.quantity = quantity
        self.constituents = constituents
    
    def __str__(self):
        return f'Recipe({self.constituents} => {self.quantity} {self.element}'
    
    def __repr__(self):
        return str(self)


def parse_recipe(s):
    def helper(data):
        quantity, element = data.strip().split() 
        return element, int(quantity)
    
    constituents, element_info = s.split('=>')
    condi = {}
    for constituent in constituents.strip().split(','):
        element, quantity = helper(constituent)
        condi[element] = quantity
    
    element, quantity = helper(element_info)
    return Recipe(element, quantity, condi)


# return the number of ore required to create quantity
# of element with given recipes and leftover material
def chem_reaction(element, quantity, recipes, leftover):
    # if this is a ore, we cannot produce it from any
    # recipe so just return the quantity
    if element == 'ORE': return quantity

    # if there is element remaining in leftover, see how
    # much we can use, if we can have enough left thats great,
    # no more ores are needed, otherwise we will synthesize the
    # remaining quantity
    leftover_quantity = leftover[element]
    assert leftover_quantity >= 0

    if leftover_quantity >= quantity:
        leftover[element] -= quantity
        return 0
    else:
        quantity -= leftover_quantity
        leftover[element] = 0
    
    # we are here, which means quantity needed to synthesize is > zero
    # use the recipe to synthesize the element and update leftovers
    assert quantity > 0

    # can only synthesize the element in recipe.quantity
    # need quantity of the element, find a factor such that
    # we have factor * recipe.quantity >= quantity
    recipe = recipes[element]
    num_times = math.ceil(quantity / recipe.quantity)
    produce_quantity = num_times * recipe.quantity
    total_ore = 0

    # we are left with the rest of the element if any
    leftover[element] = produce_quantity - quantity
 
    # the whole reaction is multiplied by factor that means
    # every constituent element is also needed in that factor
    for c_element, c_quantity in recipe.constituents.items():
        total_ore += chem_reaction(c_element, num_times * c_quantity, recipes, leftover)

    return total_ore


# given number of ore, how much fuel can be produced
# break it down as a binary search problem and ask the
# question in reverse, what amount of fuel would be required
# to need this many ore, as this computation is easier
def max_fuel_produced(ore, recipes):
    lo, hi = 0, 1e12
    max_fuel = -1

    while lo < hi:
        mid = lo + (hi - lo) // 2
        ores_needed = chem_reaction('FUEL', mid, recipes, defaultdict(int))

        if ores_needed <= ore:
            lo = mid + 1
            max_fuel = max(max_fuel, mid)
        elif ores_needed > ore:
            hi = mid - 1
    
    return max_fuel


def main():
    recipes = {}
    with open('d14.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                recipe = parse_recipe(line)
                recipes[recipe.element] = recipe

    # part 1
    # ore = chem_reaction('FUEL', 1, recipes, defaultdict(int))
    # print(ore)

    # part 2
    fuel = max_fuel_produced(1000000000000, recipes)
    print(fuel)


main()
