import sys
import re
import itertools

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/22.txt'
X = [line.replace('\n','') for line in open(input_file)]


RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

directions = X[-1]

map = X[:-2]
# Add padding in.
max_length = max(len(r) for r in map)
for i, r in enumerate(map):
  map[i] = r + ' ' * (max_length - len(r))


def parse_directions(d):
  d = '_' + d
  for turn, steps in zip(re.findall(r'L|R|_', d), re.findall(r'\d+', d)):
    yield (turn, int(steps))

def path(loc, facing, map):
  """Returns the path of (x,y) coordinates to traverse."""
  p = []
  if facing == RIGHT:
      p = [(loc[0],y) for y in range(len(map[0])) if map[loc[0]][y] != ' ']
      p = p[p.index(loc)+1:] + p[:p.index(loc)+1]    
  elif facing == LEFT:
    p = [(loc[0],y) for y in range(len(map[0])) if map[loc[0]][y] != ' ']
    p = p[p.index(loc):] + p[:p.index(loc)]
    p.reverse()
  
  elif facing == DOWN:
    p = [(x,loc[1]) for x in range(len(map)) if map[x][loc[1]] != ' ']
    p = p[p.index(loc)+1:] + p[:p.index(loc)+1]
    
  elif facing == UP:
    p = [(x,loc[1]) for x in range(len(map)) if map[x][loc[1]] != ' ']
    p = p[p.index(loc):] + p[:p.index(loc)]
    p.reverse()
  return p

def part1(directions, map):
  loc = (0, map[0].find('.'))
  facing = RIGHT
  
  for turn, steps in parse_directions(directions):
    if turn == 'R':
      facing = (facing + 1) % 4
    elif turn == 'L':
      facing = (facing -1) % 4
      
    p = path(loc, facing, map)
      
    for i, (x,y) in enumerate(itertools.cycle(p)):
      if map[x][y] == '#' or i == steps:
        break
      loc = (x,y)
      
    # print('New location:', loc[0]+1, loc[1]+1)
  
  # print((loc[0]+1,loc[1]+1,facing))
  return (1000 * (loc[0]+1)) + (4 * (loc[1]+1)) + facing

print(part1(directions, map))
