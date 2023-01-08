import sys
import time

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/elves_1.txt'
X = [line.strip() for line in open(input_file)]

p1 = []
t = 0

for x in X:
  if x == '':
    p1.append(t)
    t = 0
  else:
    t += int(x)
    
print(sorted(p1, reverse=True)[0])
print(sum(sorted(p1, reverse=True)[0:3]))
