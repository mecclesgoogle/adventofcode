from copy import copy
from collections import defaultdict, deque
import math
import re
import sys
from itertools import cycle

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/20.txt'
X = [int(line.strip()) for line in open(input_file)]


def mix(input:list[int], n=1, m=1):
  """Returns mixed list of integers."""
  length = len(input)
  
  input = [(i, val*m) for (i,val) in enumerate(input)]
  result = copy(input)
  for _ in range(n):
    for i, val in input:
      if val == 0:
        continue
      currentindex = result.index((i, val))
      result.remove((i, val))
      newindex = currentindex + val
      if newindex >= length:
        newindex %= (length - 1 )
      elif newindex < 0:
        newindex %= (length - 1)

      result.insert(newindex, (i, val))

  return [val for (_, val) in result]

def coordinatesv1(stopval: int, a:list[int]):
  i = a.index(stopval)
  return [a[i + n] for n in [1000,2000,3000]]  


# Fun way of doing it using cycle(), but totally unecessary.
def coordinates(stopval: int, a:list[int]):
  """Generates coordinates."""
  startindex = None
  for i, x in enumerate(cycle(a)):
    if startindex is not None and i == startindex + 1000:
      yield x
    if startindex is not None and i == startindex + 2000:
      yield x
    if startindex is not None and i == startindex + 3000:
      yield x
      break
    if startindex is None and x == stopval:
      startindex = i


print(sum(list(coordinatesv1(0, mix(X)))))
print(sum(list(coordinatesv1(0, mix(X, 10, 811589153)))))
