import math
from collections import defaultdict

def lcm(x, y):
    return (x * y) // math.gcd(x, y)


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

def get_ores_for_quantity(element, ore_info, needed_quantity):
    steps = 1
    while (steps * ore_info[element]) < needed_quantity:
        steps += 1
    return ore_info[element] * steps

def chem_reaction(element, quantity, recipes, leftover):
    # can't manufacture ore
    if element == 'ORE':
        return quantity
    # elif 'ORE' in recipe.constituents:
    #     return = {'ORE': recipe.constituents['ORE'],
    #               element: recipe.quantity}
    else:
        total_ore = 0
        recipe = recipes[element]
        left_quantity = leftover[element] if element in leftover else 0

        synthesis_needed = quantity
        if left_quantity >= synthesis_needed:
            synthesis_needed = 0
            leftover[element] -= quantity
        else:
            synthesis_needed -= left_quantity
            leftover[element] = 0

        if synthesis_needed > 0:
            for celement, quantity in recipe.constituents.items():
                one_reaction = chem_reaction(celement, quantity, recipes, leftover)
                # get as much ore as is needed, one reaction may not be enough
                synthesized = get_ores_for_quantity(celement, ore_info, quantity)
                print(ore_info)
                total_ore += ore_info['ORE']

                # synthesized more than needed, update leftover
                if ore_info[celement] > quantity:
                    leftover[celement] += ore_info[celement] - quantity
        
        return total_ore


def main():
    recipes = {}
    with open('d14.txt') as fin:
        for line in fin:
            line = line.strip()
            if line:
                recipe = parse_recipe(line)
                recipes[recipe.element] = recipe

    x = chem_reaction('FUEL', recipes, {}, defaultdict(int))
    print(x)


main()
