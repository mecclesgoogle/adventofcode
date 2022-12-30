import sys
import collections
import functools

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/24.txt'
X = [line.replace('\n','') for line in open(input_file)]

MAP = collections.defaultdict(list)
for x, line in enumerate(X):
  for y, character in enumerate(line):
    if character != '.' and character != '#':
      MAP[(int(x),int(y))] = character
      
START = (0, X[0].index('.'))
DEST = (len(X)-1, X[len(X)-1].index('.'))
HEIGHT = len(X) -2
WIDTH = len(X[0]) - 2    

@functools.cache
def blocked(turn: int) -> set:
  locs = set()
  for loc, blizzard in MAP.items():
    if blizzard == '>':
      locs.add((loc[0],(loc[1]+turn-1) % WIDTH + 1))
    elif blizzard == '<':
      locs.add((loc[0],WIDTH + (loc[1] - turn) % -WIDTH))
    elif blizzard == 'v':
      locs.add(((loc[0]+turn-1)%HEIGHT + 1,loc[1]))
    elif blizzard == '^':
      locs.add((HEIGHT + (loc[0] - turn) % -HEIGHT,loc[1]))

  locs.update([(0,y) for y in range(len(X[0])) if (0,y) != START])
  locs.update([(len(X)-1,y) for y in range(len(X[0])) if (len(X)-1,y) != DEST])
  locs.update([(x,0) for x in range(len(X))])
  locs.update([(x,len(X[0])-1) for x in range(len(X))])
  return locs


def bfs_solution(start, end):
  traversals =  0
  queue = collections.deque([(start, 0)])
  visited = set()
  while queue:
    (loc, turn) = queue.popleft()
    if (loc, turn) in visited:
      continue # skip dupe paths
    (x,y) = loc
    visited.add((loc, turn))
    if loc == end:
      queue = collections.deque([(loc, turn)])
      traversals += 1
      end=start
      start=loc
      visited.clear()
      if traversals == 1:
        print(turn)
        continue
      elif traversals == 2:
        continue
      elif traversals == 3:
        print(turn)
        break
    blizzards = blocked(turn+1)
    if x == 0:
      if (1,y) not in blizzards:
        queue.append(((1,y), turn+1)) # We are at the start; always move down if possible.
      else:
        queue.append((loc, turn+1)) # STAY
    elif x == HEIGHT+1:
      if (HEIGHT,y) not in blizzards:
        queue.append(((HEIGHT,y), turn+1)) # We are at the start; always move up if possible.
      else:
        queue.append((loc, turn+1)) # STAY
    else:
      if x > 0 and (x-1,y) not in blizzards:
        queue.append(((x-1,y), turn+1)) # UP
      if (x+1,y) not in blizzards:
        queue.append(((x+1,y), turn+1)) # DOWN
      if (x,y-1) not in blizzards:
        queue.append(((x,y-1), turn+1)) # LEFT
      if (x,y+1) not in blizzards:
        queue.append(((x,y+1), turn+1)) # RIGHT
      if (x,y) not in blizzards:
        queue.append((loc, turn+1)) # STAY
      

bfs_solution(START, DEST)