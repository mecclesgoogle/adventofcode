import copy
import sys

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/elves_14.txt'
X = [line.strip() for line in open(input_file)]
MAP = []
PATHS = []
X_START = 1000
Y_START = 0
X_END = Y_END = 0
for i, v in enumerate(X):
  path = v.split(' -> ')
  path = [p.split(',') for p in path]
  path = [[int(p[0]),int(p[1])] for p in path]
  X_START = min(X_START, min([x[0] for x in path])) - 1 # allow overflow for P2
  X_END = max(X_END, max([x[0] for x in path])) + 1 # allow overflow for P2
  Y_END = max(Y_END, max([x[1] for x in path]))
  PATHS.append(path)

MAP = [['.' for _ in range(0, X_END+1)] for _ in range(0, Y_END+1)]
    
# Draw rocks
for path in PATHS:
  for i, edge in enumerate(path):
    if i == len(path) - 1:
      MAP[edge[1]][edge[0]] = '#'
      break # reached end of rock path
    dest = path[i+1]
    if edge[0] == dest[0]: # draw y
      for y in range(edge[1], dest[1], 1 if dest[1] > edge[1] else -1):
        MAP[y][edge[0]] = '#'
    else: # draw x
      for x in range(edge[0], dest[0], 1 if dest[0] > edge[0] else -1):
        MAP[edge[1]][x] = '#'   
    

def drop_sand(map) -> bool:
  sand = (0,500)
  while map[sand[0]+1][sand[1]] == '.' or map[sand[0]+1][sand[1]-1] == '.' or map[sand[0]+1][sand[1]+1] == '.':
    # we can move
    if map[sand[0]+1][sand[1]] == '.':
      sand = (sand[0] + 1, sand[1])  # Down
    elif map[sand[0]+1][sand[1]-1] == '.':
      sand = (sand[0] + 1, sand[1]-1)  # Down and Left
    else:
      sand = (sand[0] + 1, sand[1]+1)  # Down and Right
  
  map[sand[0]][sand[1]] = '+'
  return sand != (0,500)
  
p1 = copy.deepcopy(MAP)
S = 0
D = True
while(D):
  try:
    D = drop_sand(p1)
  except IndexError:  # Lazy way of knowing we hit floor
    break
  S += 1

print(S)

# Part 2
p2 = MAP
p2.append(['.' for _ in range(0, X_END+1)])
p2.append(['#' for _ in range(0, X_END+1)])
Y_END += 2

S = 0
D = True
while (D):
  D = drop_sand(p2)
  S += 1

print(S)