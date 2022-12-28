import sys

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/23.txt'
X = [line.replace('\n','') for line in open(input_file)]

ELVES = set()

for x, line in enumerate(X):
  for y, c in enumerate(line):
    if c == '#':
      ELVES.add((x,y))

def next_move(elf, elves, direction):
  if set([(elf[0]-1, elf[1]-1), (elf[0]-1, elf[1]), (elf[0]-1, elf[1]+1),
          (elf[0]+1, elf[1]-1), (elf[0]+1, elf[1]), (elf[0]+1, elf[1]+1),
          (elf[0],elf[1]-1),(elf[0],elf[1]+1)]).isdisjoint(elves):
    return None
  
  if direction == 'N':
    if set([(elf[0]-1, elf[1]-1), (elf[0]-1, elf[1]), (elf[0]-1, elf[1]+1)]).isdisjoint(elves):
      return (elf[0]-1,elf[1])
  if direction == 'S':
    if set([(elf[0]+1, elf[1]-1), (elf[0]+1, elf[1]), (elf[0]+1, elf[1]+1)]).isdisjoint(elves):
      return (elf[0]+1,elf[1])
  if direction == 'W':
    if set([(elf[0]-1, elf[1]-1), (elf[0], elf[1]-1), (elf[0]+1, elf[1]-1)]).isdisjoint(elves):
      return (elf[0],elf[1]-1)
  if direction == 'E':
    if set([(elf[0]-1, elf[1]+1), (elf[0], elf[1]+1), (elf[0]+1, elf[1]+1)]).isdisjoint(elves):
      return (elf[0],elf[1]+1)

def propose_moves(elves: set, directions = ['N','S','W','E']) -> dict:
  proposals = {}
  for elf in elves:
    for direction in directions:
      possible = next_move(elf, elves, direction)
      if possible is not None:
        proposals[elf] = possible
        break
  return proposals
 
  
def part1():
  minx = min(x for (x,_) in ELVES)
  maxx = max(x for (x,_) in ELVES)+1
  miny = min(y for (_,y) in ELVES)
  maxy = max(y for (_,y) in ELVES)+1
  return ((maxx-minx) * (maxy-miny))-len(ELVES)
 
for i in range(10000):
  if i == 10:
    print(part1())
  
  proposals = None
  if i % 4 == 0:
    proposals = propose_moves(ELVES, ['N','S','W','E'])
  elif i % 4 == 1:
    proposals = propose_moves(ELVES, ['S','W','E','N'])
  elif i % 4 == 2:
    proposals = propose_moves(ELVES, ['W','E','N','S'])
  elif i % 4 == 3:
    proposals = propose_moves(ELVES, ['E','N','S','W'])
    
  if len(proposals) == 0:
    print(f'No elves needed to move on round {i+1}')
    break
    
  
  for k, v in proposals.items():
    if sum(value == v for value in proposals.values()) == 1:
      ELVES.remove(k)
      assert v not in ELVES
      ELVES.add(v)
