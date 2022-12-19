import sys
from collections import deque

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/18.txt'
X = [line.strip() for line in open(input_file)]

cubes = set()

for line in X:
  x,y,z = [int(x)for x in line.split(',')]
  cubes.add((x,y,z))

def get_adjacent_coords(c):
  return [
        (c[0]+1,c[1],c[2]),
        (c[0]-1,c[1],c[2]),
        (c[0],c[1]+1,c[2]),
        (c[0],c[1]-1,c[2]),
        (c[0],c[1],c[2]+1),
        (c[0],c[1],c[2]-1),
    ]

total = 6 * len(cubes)
for cube in cubes:
  for c in get_adjacent_coords(cube):
    total -= 1 if c in cubes else 0
  
print(total)

# In part 2 we exclude interior sides

# Calculate the edges.
x_edges = set([min([n[0] for n in cubes]),max([n[0] for n in cubes])])
y_edges = set([min([n[1] for n in cubes]),max([n[1] for n in cubes])])
z_edges = set([min([n[2] for n in cubes]),max([n[2] for n in cubes])])
  
def surface_coords(c, cubes):
  return [c for c in get_adjacent_coords(c) if c not in cubes]

cache = {}
def find_edge(visited, cubes, cube):
  if cube in cache:
    return cache[cube]
  visited = {cube}
  queue = deque(visited)
  
  while queue:
    c = queue.popleft()
    for n in get_adjacent_coords(c):
      if n not in visited:
        if n[0] in x_edges and n[1] in y_edges and n[2] in z_edges:
          cache[cube] = True
          return True
        if n not in cubes:
          visited.add(n)
          queue.append(n)
  cache[cube] = False
  return False

p2 = 0
for cube in cubes:
  visited = set()
  queue = deque()
  for c in  surface_coords(cube, cubes):
    p2 += 1 if find_edge(visited, cubes, c) else 0
    
print(p2)