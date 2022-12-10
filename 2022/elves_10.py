import sys

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/elves_10.txt'

X = 1
C = 1
T = 0

def is_checkpoint(c: int) -> bool:
  return (c - 20) % 40 == 0

f = open(input_file, 'r')
for line in f:
  p = line.strip().split(' ')
  if p[0] == 'noop':
    C += 1
    T += X * C if is_checkpoint(C) else 0
  else:
    C += 1
    if is_checkpoint(C):
      T += X * C
    C += 1
    X += int(p[1])
    T += X * C if is_checkpoint(C) else 0

  
print(T)

# Part 2
X = 1
C = -1
CRT = [['' for _ in range(40)] for _ in range(6)]

def draw(crt: list[list[str]], x:int, c:int):
  """Mutates crt."""
  crt[c//40][c%40] = '#' if abs(c%40 - x) <= 1 else '`'

f = open(input_file, 'r')
for line in f:
  p = line.strip().split(' ')
  if p[0] == 'noop':
    C += 1
    draw(CRT, X, C)
  else:
    C += 1
    draw(CRT, X, C)
    C += 1
    draw(CRT, X, C)
    X += int(p[1])

for i in range(6):
  print(''.join(CRT[i]))