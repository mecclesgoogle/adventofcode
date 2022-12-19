import sys
import time

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/17.txt'
X = [line.strip() for line in open(input_file)]

# Rocks are modelled as relative coords starting at the top left corner.
ROCKS = [ # x,y pairs
  set([(0,0),(1,0),(2,0),(3,0)]),
  set([(1,0),(0,1),(1,1),(2,1), (1,2)]),
  set([(2,2),(2,1),(0,0),(1,0),(2,0)]),
  set([(0,0),(0,1),(0,2),(0,3)]),
  set([(0,0),(1,0),(0,1),(1,1)]),
]

WIND = X[0]
TURN = 0
TOP = 0
ROCK_COUNT = 0
CHAMBER_WIDTH = 7
CHAMBER = set([(x,0) for x in range(CHAMBER_WIDTH)])


def print_chamber(chamber, rock):
  for y in range(max([c[1] for c in rock]), min([c[1] for c in chamber]) -1, -1):
    for x in range(7):
      if (x,y) in chamber:
        print('#',end='')
      elif (x,y) in rock:
        print('@',end='')
      else:
        print('.',end='')
    print()

def get_new_rock(rock, y_offset):
  return set(
    [
      (c[0] + 2, c[1] + y_offset) for c in rock
    ]
  )
    
def shift_left(rock, chamber):
  if any([x==0 for (x,_) in rock]):
    return rock
  left = set([(x-1,y) for (x,y) in rock]) 
  if len(left & chamber) != 0:
    return rock
  return left

def shift_right(rock, chamber):
  if any([x==6 for (x,_) in rock]):
    return rock
  right = set([(x+1,y) for (x,y) in rock])  
  if len(right & chamber) != 0:
    return rock
  return right

def shift_down(rock, chamber):
  down = set([(x,y-1) for (x,y) in rock])
  if len(down & chamber) !=0:
    raise ValueError('Cannot move down further.')
  return down

DEBUG_MODE=False

# For part 2 we need to 

class StateCache():
  """A cache for storing previous states.
  
  The cache key comprises of:
  1. The rock type that last dropped.
  2. The position in the wind cycle. 
  3. A set of rock x,y coordinates.
  
  The value is a tuple of (wind cycle, y coord of TOP)
  """
  _cache = {}
  
  def _cache_key(self, chamber, rock_type, i):
    max_depth = 20 # Random, but deep enough.
    top = max([y for (_,y) in chamber])
    #Normalize it
    rock_formation = frozenset([(x,top-y) for (x,y) in chamber if top-y<=max_depth])
    return (rock_type, i, rock_formation)
    
  def get(self, chamber, rock_type, i):
    key = self._cache_key(chamber, rock_type, i)
    return self._cache[key] if key in self._cache else None
  
  def update(self, chamber, rock_type, i, top):
    key = self._cache_key(chamber, rock_type, i)
    self._cache[key] = (i, top)
      
cached_states = StateCache()
Y_DELTA_FROM_CACHE = 0
PART_2_LIMIT=1_000_000_000_000

while ROCK_COUNT < PART_2_LIMIT:
  rock = get_new_rock(ROCKS[ROCK_COUNT % 5], TOP + 4)
  
  while True:
    wind_dir = WIND[TURN % len(WIND)]
    if DEBUG_MODE:
      time.sleep(2)
      print('top: ', TOP)
      print('turn: ', TURN)
      print('wind dir: ', wind_dir)
      print_chamber(CHAMBER, rock)
      print()
    TURN += 1
    # Move left or right.
    if wind_dir == '<':
      rock = shift_left(rock, CHAMBER)
    else:
      rock = shift_right(rock, CHAMBER)
    # Move down  
    can_move_down = True # TODO
    try:
      rock = shift_down(rock, CHAMBER)
    except ValueError:
      can_move_down = False
    # Finished this rock, record and move on
    if not can_move_down:
      CHAMBER = CHAMBER | rock
      TOP = max([y for (_,y) in CHAMBER])
      # Part 2 cache
      if ROCK_COUNT >= 2022:
        cached_result = cached_states.get(CHAMBER, ROCK_COUNT % 5, TURN % len(WIND))
        if cached_result is not None:
          print('CAche hit')
          prev_rock_count = cached_result[0]
          prev_y = cached_result[1]
          delta_y = TOP - prev_y
          # How many rock drops we have jumped
          delta_rock_count = ROCK_COUNT - prev_rock_count 
          jump = (PART_2_LIMIT - ROCK_COUNT) // delta_rock_count
          Y_DELTA_FROM_CACHE += jump * delta_y
          # We know what the outcome is so skip ahead
          ROCK_COUNT += jump * delta_rock_count
          
        cached_states.update(CHAMBER, ROCK_COUNT % 5, ROCK_COUNT, TOP)
      
      # /Part 2 cache
      break # Next rock
  ROCK_COUNT += 1
  if ROCK_COUNT == 2022:
    print(TOP)

print(TOP+Y_DELTA_FROM_CACHE)
