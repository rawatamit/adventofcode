from cgitb import text
import re
from aocd import get_data


class Ingredient:
  def __init__(self, name, capacity, durability, flavor, texture, calories) -> None:
    self.name = name
    self.capacity = capacity
    self.durability = durability
    self.flavor = flavor
    self.texture = texture
    self.calories = calories
  
  def __str__(self) -> str:
    return f'Ingredient({self.name}, capacity={self.capacity}, ' \
           f'durability={self.durability}, flavor={self.flavor}, ' \
           f'texture={self.texture}, calories={self.calories})'
  
  def __repr__(self) -> str:
    return str(self)


def dfs(ingredients, curidx, curingr, cursum, max_teaspoons, fn=print):
  if cursum == max_teaspoons:
    fn(curingr)
  elif curidx < len(ingredients):
    for i in range(max_teaspoons+1):
      if cursum + i > max_teaspoons: break
      save = curingr[curidx]
      curingr[curidx] = i
      dfs(ingredients, curidx + 1, curingr, cursum+i, max_teaspoons, fn)
      curingr[curidx] = save


def score1(ingr, measures):
  properties = ['capacity', 'durability', 'flavor', 'texture']
  tot_score = 1
  for prop in properties:
    this_prop = 0
    for i, ing in enumerate(ingr):
      this_prop += getattr(ing, prop) * measures[i]
    tot_score *= this_prop if this_prop > 0 else 0
  return tot_score


def score2(ingr, measures):
  this_prop = 0
  for i, ing in enumerate(ingr):
    this_prop += ing.calories * measures[i]
  if this_prop != 500: return 0
  
  properties = ['capacity', 'durability', 'flavor', 'texture']
  tot_score = 1
  for prop in properties:
    this_prop = 0
    for i, ing in enumerate(ingr):
      this_prop += getattr(ing, prop) * measures[i]
    tot_score *= this_prop if this_prop > 0 else 0
  return tot_score


def main():
  data = '''Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
'''.strip()
  data = get_data(year=2015, day=15)
  pattern = r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (\d+)'
  ingredients = []
  for line in data.split('\n'):
    ingr, cap, dur, flav, text, cal = re.findall(pattern, line)[0]
    ingredients.append(Ingredient(ingr, int(cap), int(dur), int(flav), int(text), int(cal)))
  #print(ingredients)
  #curingr = [0] * len(ingredients)
  #dfs(ingredients, 0, curingr, 0, 4)

  # part 1
  max_teaspoons = 100
  curingr = [0] * len(ingredients)
  scores = []
  score_fn1 = lambda measures: scores.append(score1(ingredients, measures))
  dfs(ingredients, 0, curingr, 0, max_teaspoons, fn=score_fn1)
  print(max(scores))

  max_teaspoons = 100
  curingr = [0] * len(ingredients)
  scores = []
  score_fn2 = lambda measures: scores.append(score2(ingredients, measures))
  dfs(ingredients, 0, curingr, 0, max_teaspoons, fn=score_fn2)
  print(max(scores))


main()
