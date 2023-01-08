import math
import numpy as np
import sys

input_file = sys.argv[1] if len(sys.argv) > 1 else 'elves_9.txt'

directions = {'U': [0,1], 'D': [0,-1],'L': [-1,0],'R':[1,0]}

H = (0,0)
T = (0,0)
TRAIL = set()


def move_tail(h: tuple[int,int], t: tuple[int,int]) -> tuple[int,int]:
  """Returns new coords of tail."""
  x_d = h[0] - t[0] # x delta
  y_d = h[1] - t[1] # y delta
  diff = math.dist(h, t)
  if abs(diff) < 2: # euclidean distance <2 means adjacency
    return t
  elif abs(x_d) >= 2 and abs(y_d) >=2: # Can happen if tail follows tail diagonally (part 2)
    return (h[0]+1 if h[0] < t[0] else h[0]-1, h[1]+1 if h[1] < t[1] else h[1]-1)
  elif abs(x_d) >= 2:
    return (h[0]+1 if h[0] < t[0] else h[0]-1, h[1])
  elif abs(y_d) >= 2:
    return (h[0], h[1]+1 if h[1] < t[1] else h[1]-1)
  assert False

f = open(input_file, 'r')
for line in f:
  parts = line.strip().split(' ')
  direction = parts[0]
  steps = int(parts[1])
  for _ in range(steps):
    H = tuple(np.add(H, directions[direction])) # Move head
    T = move_tail(H, T)
    TRAIL.add(T) # set type will take care of duplicates

print(len(TRAIL))

# Part 2
T = [(0,0) for _ in range(0,10)] # T[0] = head, T[9] = end tail
TRAIL = set()
f = open(input_file, 'r')
for line in f:
  parts = line.strip().split(' ')
  direction = parts[0]
  steps = int(parts[1])
  for _ in range(steps):
    T[0] = tuple(np.add(T[0], directions[direction])) # Move head
    for i in range(1,10):
      T[i] = move_tail(T[i-1],T[i])
      if i == 9:
        TRAIL.add(T[9])


print(len(TRAIL))
