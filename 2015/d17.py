from aocd import get_data


def dfs(capacities, curcap, curidx, total, numcontainers, containers, liters):
  if total == liters:
    #print(curcap, numcontainers)
    containers.append(numcontainers)
    return
  
  if curidx >= len(capacities):
    return
  
  # take curidx if possible
  if capacities[curidx] + total <= liters:
    save = curcap[curidx]
    curcap[curidx] = capacities[curidx]
    dfs(capacities, curcap, curidx + 1, total + capacities[curidx], numcontainers + 1, containers, liters)
    curcap[curidx] = save

  # don't take curidx
  dfs(capacities, curcap, curidx + 1, total, numcontainers, containers, liters)


if __name__ == '__main__':
  data = '20\n15\n10\n5\n5'
  data = get_data(year=2015, day=17)
  capacities = [int(x) for x in data.split('\n')]
  #print(capacities)
  liters = 150
  curcap = [0] * len(capacities)
  containers = []
  dfs(capacities, curcap, 0, 0, 0, containers, liters)
  print(containers.count(min(containers)))
