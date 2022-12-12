from collections import deque 
import sys

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/elves_12.txt'

X = [line.strip() for line in open(input_file)]

S = None
E = None

# Find S, E and replace them with actual altitude.
for i in range(0, len(X)):
  if 'S' in X[i]:
    S = (i, X[i].index('S'))
    X[i] = X[i].replace('S', 'a')
  if 'E' in X[i]:
    E = (i, X[i].index('E'))
    X[i] = X[i].replace('E', 'z')


def traversible_nodes(node: tuple[int,int]) -> list[tuple[int,int]]:
  """Returns list of nodes that can be reached."""
  v = []
  global X
  if node[0] != 0:
    if ord(X[node[0]-1][node[1]]) - ord(X[node[0]][node[1]]) <= 1:
      v.append((node[0]-1, node[1]))
  if node[1] != len(X[0])-1:
    if ord(X[node[0]][node[1]+1]) - ord(X[node[0]][node[1]]) <= 1:
      v.append((node[0], node[1]+1))
  if node[0] != len(X)-1:
    if ord(X[node[0]+1][node[1]]) - ord(X[node[0]][node[1]]) <= 1:
      v.append((node[0]+1, node[1]))
  if node[1] != 0:
    if ord(X[node[0]][node[1]-1]) - ord(X[node[0]][node[1]]) <= 1:
      v.append((node[0], node[1]-1))
  return v


def solve(start: tuple[int,int]):
  q = deque()  
  q.appendleft(start)
  v = set()
  v.add(start)
  global N
  prev={}
  for i in range(len(X)):
    for j in range(len(X[0])):
      prev[(i,j)] = None
  while len(q) > 0:
    n = q.popleft()
    vs = traversible_nodes(n)
    for p in vs:
      if p not in v:
        q.append(p)
        v.add(p)
        prev[(p[0],p[1])] = n
  return prev
    

def reconstructPath(start: tuple[int,int], end: tuple[int,int], prev: list[tuple[int,int]]):
  path = [end]
  at = prev[end]
  while(at is not None):
    path.append(at)
    at = prev[at]
    
  path.reverse()
  if path[0] == start:
    return len(path) - 1


def search(start: tuple[int,int], end: tuple[int,int]):
  prev = solve(start)  
  return reconstructPath(start, end, prev)
  
print(search(S, E))
  
# Part 2

distances = set()
for i in range(len(X)):
  for j in range(len(X[0])):
    if X[i][j] == 'a':
      distance = search((i,j), E)
      if distance is not None:
        distances.add(distance)
          
print(min(distances))