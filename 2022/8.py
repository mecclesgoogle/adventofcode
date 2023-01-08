import sys

input_file = sys.argv[1] if len(sys.argv) > 1 else 'elves_8.txt'
X = [line.strip() for line in open(input_file)]

width = len(X[0])
height = len(X)

def is_visible(X, x, y) -> bool:
  """Returns True if a tree at x,y is visible."""
  val = int(X[x][y])
  if x == 0 or x == height-1 or y == 0 or y == width -1:
    return True # Edge node
  
  # Check left to right
  visible = True
  for i in range(0,y):
    if int(X[x][i]) >= val:
      visible = False
  if visible:
    return True
  # Check right to left
  visible = True
  for i in range(width-1,y,-1):
    if int(X[x][i]) >= val:
      visible = False
  if visible:
    return True

  # check top to bottom
  visible = True
  for i in range(0,x):
    if int(X[i][y]) >= val:
      visible = False
  if visible:
    return True

  # check bottom to top
  visible = True
  for i in range(height-1,x,-1):
    if int(X[i][y]) >= val:
      visible = False
  if visible:
    return True

count = 0
for x in range(0, height):
  t=-1
  for y in range(0,width):
    if is_visible(X, x, y):
      count +=1

print(count)

# Part 2

def score(X, x, y):
  """Returns scenic score for tree at x,y."""
  if x == 0 or x == height-1 or y == 0 or y == width -1:
    # Edge node
    return 0
  # Look all around and count how far we go till a tree >= it's size is found
  val = int(X[x][y])
  
  # Check left
  l_vis = 0
  for i in range(y-1,-1,-1):
    l_vis +=1 
    if int(X[x][i]) >= val:
      break
  # Check right
  r_vis = 0
  for i in range(y+1,width):
    r_vis +=1 
    if int(X[x][i]) >= val:
      break

  # check down
  d_vis = 0
  for i in range(x+1,height):
    d_vis +=1 
    if int(X[i][y]) >= val:
      break

  # check up
  u_vis = 0
  for i in range(x-1,-1,-1):
    u_vis +=1 
    if int(X[i][y]) >= val:
      break
  
  return l_vis * r_vis * d_vis * u_vis

max_score = 0
for x in range(0, height):
  for y in range(0,width):
    s = score(X, x, y)
    max_score=max(max_score, score(X, x, y))


print(max_score)