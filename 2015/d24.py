from aocd import get_data
from functools import reduce
import re


def make_subsets(subset, total, nums, curidx, subsets):
  if sum(subset) == total:
    subsets.append(subset[:])
  elif curidx < len(nums):
    n = nums[curidx]
    # put n in s1
    if sum(subset) + n <= total:
      subset.append(n)
      make_subsets(subset, total, nums, curidx + 1, subsets)
      subset.pop()
    
    make_subsets(subset, total, nums, curidx + 1, subsets)


if __name__ == '__main__':
  data = re.sub(' ', '\n', '1 2 3 4 5 7 8 9 10 11')
  data = get_data(year=2015, day=24)
  nums = [int(x) for x in data.splitlines()]

  # Assumes that the subsets can be divided with the min qe set.
  # This doesn't hold true for all cases, the input allows this.

  part1 = False
  if part1:
    assert sum(nums) % 3 == 0
    subsets = []
    make_subsets([], sum(nums) // 3, nums, 0, subsets)
    min_len = len(min(subsets, key=lambda subset: len(subset)))
    min_subsets = filter(lambda subset: len(subset) == min_len, subsets)
    qe = map(lambda subset: reduce(lambda x, y: x * y, subset), min_subsets)
    print(min(qe))
  else:
    assert sum(nums) % 4 == 0
    subsets = []
    make_subsets([], sum(nums) // 4, nums, 0, subsets)
    min_len = len(min(subsets, key=lambda subset: len(subset)))
    min_subsets = filter(lambda subset: len(subset) == min_len, subsets)
    qe = map(lambda subset: reduce(lambda x, y: x * y, subset), min_subsets)
    print(min(qe))
