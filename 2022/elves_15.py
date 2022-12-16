#!/usr/bin/python3
import re
import sys


infile = sys.argv[1] if len(sys.argv)>1 else '/Users/markeccles/adventcode/2022/elves_15.txt'
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]

S_D = {} # Sensor loc -> distance to closest beacon
S_B = {} # Sensor loc -> closest beacon loc
B = set() # all beacon locations (for filtering)

def mdist(ax:int,ay:int,bx:int,by:int) -> int:
  return abs(ax-bx) + abs(ay-by)


for line in lines:
  n = re.findall(r'-?\d+', line)
  sx,sy,bx,by = int(n[0]),int(n[1]),int(n[2]),int(n[3])
  S_D[sx,sy] = mdist(sx,sy,bx,by)
  S_B[sx,sy] = bx,by
  B.add((bx,by))


Y=2000000
not_b=set()
beacon_x = set()
# Loop all of the sensors
for point, dist in S_D.items():
  sx, sy = point
  bx, by = S_B[sx, sy]
  if by == Y: # Beacon on same row
    beacon_x.add(bx)
  overlap_amount = dist - abs(Y-sy)
  if overlap_amount > 0: # the sensor's radius overlaps Y.
    not_b.update([x for x in range(sx-overlap_amount, sx+overlap_amount+1)])
bY = set([b[0] for b in B if b[1] == Y])
not_b.difference_update(bY)
print(len(not_b))

# Part 2
X = Y = 4000000

def part2():
  global S_D
  checked_locs = set()
  for loc, dist in S_D.items():
    sx,sy = loc
    # scan edges of each Sensor (there are dist + 1 edges)
    # this is less checks than 4e6 * 4e6 (16 trillion)
    for edge in ['TR','TL','BL','BR']:
      for i in range(0,dist+1):
        if edge == 'BR':
          x = sx + dist + 1 - i
          y = sy + i
        elif edge =='BL':
          x = sx - i
          y = sy + dist + 1 - i
        elif edge == 'TL':
          x = sx - dist - 1 + i
          y = sy - i
        elif edge == 'TR':
          x = sx + i
          y = sy - dist - 1 + i
  
        if (0 <= x <= X and 0 <= y <= Y
            and (x, y) not in checked_locs):
          # If (cx,cy) is further away from all sensors radius then that must be it.
          outofrange = all(mdist(x,y,ox,oy) > other_dist 
                      for (ox, oy), other_dist in S_D.items())
        if outofrange:
          return (X * x) + y
        else:
          checked_locs.add((x, y))
          
print(part2())