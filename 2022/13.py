from functools import cmp_to_key
import math
import sys
from typing import Any

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/elves_13.txt'

X = [line.strip() for line in open(input_file)]


def compare(l: Any, r: Any) -> int:
  lt = type(l)
  rt = type(r)
  if lt == int and rt == int:
    return (l > r) - (l < r)
  elif lt == list and rt == list:
    i = 0
    while i < len(l) and i < len(r):
      c = compare(l[i], r[i])
      if c != 0:
        return c
      i += 1
    if i == len(l) and i < len(r):
      return -1 # l ran out
    elif i == len(r) and i < len(l):
      return 1 # r ran out
    else:
      return 0 # end of both lists
  elif lt == int and rt == list:
    return compare([l], r)
  elif lt == list and rt == int:
    return compare(l, [r])
  assert False # Shouldn't happen

R = 0
P = [[[2]],[[6]]]

for i in range(0, len(X), 3):
  l = eval(X[i])
  r = eval(X[i+1])
  P += [l, r] # For part 2
  if compare(l, r) == -1:
    R += (i // 3) +1
  
print(R)
  
# Part 2
P = sorted(P, key=cmp_to_key(lambda l,r: compare(l,r)))
R=[]
for i in range(0, len(P)):
  if P[i] == [[2]] or P[i] == [[6]]:
    R.append(i+1) 
    
print(math.prod(R))