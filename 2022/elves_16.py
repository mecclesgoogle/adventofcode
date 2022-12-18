import copy
from itertools import permutations
import re
import sys
from collections import deque

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/elves_16.txt'
X = [line.strip() for line in open(input_file)]

# BFS
visited = [] # List to keep track of visited nodes.
queue = []     #Initialize a queue

def bfs(visited:list[str], graph, node:str) -> list[str]:
  visited.append(node)
  queue.append(node)
  prev={}

  while queue:
    s = queue.pop(0) 
    # prev.append(s)

    for neighbour in graph[s][1]:
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)
        prev[neighbour] = s
  return prev


def reconstructPath(v1:str,v2:str,prev:list[str]) -> int:
  path = [v2]
  at = prev[v2]
  while(at is not None):
    path.append(at)
    at = prev[at] if at in prev else None
    
  path.reverse()
  if path[0] == v1:
    return len(path) - 1


def search(v1:str, v2:str, graph) -> int:
  """Returns distance from v1 to v2"""
  prev = bfs([], graph, v1)  
  return reconstructPath(v1, v2, prev)

# /BFS

def parse_input(lines: list[str]):
  graph = {}
  for line in lines:
    s = line.split()
    v = s[1]
    r = int(re.findall(r'\d+', s[4])[0])
    i=9
    paths = []
    while (i < len(s)):
      paths.append(s[i].replace(',', ''))
      i += 1
    graph[v] = (r, paths)
  return graph


def reduce(graph: dict[str: tuple[str,int,list[str]]]):
  reduced_graph = {}
  valid_valves = [k for k,v in graph.items() if v[0] > 0] + ['AA']
  for v in valid_valves:
    reduced_graph[v] = []
    for o in valid_valves:
      if v == o:
        continue
      d = search(v, o, graph)
      reduced_graph[v].append((o, d))
  return reduced_graph
      
g = parse_input(X)
rates = {k:v[0] for k,v in g.items()}
reduced_graph = reduce(g)
best = None
scores = set()
def explore(open, pos, tr, score):
  global reduced_graph
  global rates
  possible_targets = [v for v in reduced_graph[pos] if v[0] not in open]
  for dest in possible_targets:
    if tr - dest[1] - 1 > 0:
      explore(open + [dest[0]], 
              dest[0], 
              tr - dest[1] - 1, 
              score + rates[dest[0]] * (tr - dest[1] - 1))
  scores.add(score)
  
explore(['AA'], 'AA', 30, 0)
print(max(scores))

# Part 2

# TODO
