import re
import sys
from collections import defaultdict
from functools import reduce

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/elves_11.txt'

INSPECTED = defaultdict(int)
INVENTORY = defaultdict(list)
TESTS = []

class Item():
  def __init__(self, w):
    self.initial = w
    self.latest = w

  def __repr__(self):
    return f'{self.initial}->{self.latest}'

  def new_worry(self, w):
    self.latest = w
  
  def reduce(self, denominators):
    p = reduce((lambda x, y: x * y), denominators)
    b = self.latest
    self.latest = self.latest % p


X = [line.strip() for line in open(input_file)]
for r in range(10000): # n rounds
  for l in range(0, len(X), 7):
    m = X[l][-2:-1]
    operator = X[l+2].split()[-2:-1][0] # * or +
    operand = X[l+2].split()[-1:][0] # old or an int
    test = int(X[l+3].split()[-1:][0]) # Divisible by x
    
    if_true = X[l+4].split()[-1:][0] # Throw to if true
    if_false = X[l+5].split()[-1:][0] # Throw to if true
 
    # Starting items
    if r == 0:
      n = re.findall(r'\d+', X[l+1])
      n = [int(x) for x in n]
      INVENTORY[m] = [Item(w) for w in n] + INVENTORY[m]
      TESTS.append(test)

    # Handle items
    for i in range(0, len(INVENTORY[m])):
      # look at items
      INSPECTED[m] += 1
      real_operand = INVENTORY[m][i].latest if operand == 'old' else int(operand)

      INVENTORY[m][i].new_worry(INVENTORY[m][i].latest + real_operand if operator == '+' else INVENTORY[m][i].latest * real_operand)
      # Bored - commented out for part 2
      # INVENTORY[m][i].new_worry(INVENTORY[m][i].latest // 3)
      # Throw items
      val = INVENTORY[m][i].latest
      if val % test == 0:
        INVENTORY[if_true].append(INVENTORY[m][i])
      else:
        INVENTORY[if_false].append(INVENTORY[m][i])
    INVENTORY[m] = [] # Threw all items
  # end of round
  # Part 2: Reset worry levels to the modulo of the product of all tests
  for v in INVENTORY.values():
    for e in v:
      e.reduce(TESTS)


for k,v in INVENTORY.items():
  print(f'{k}: {v}')

for k, v in INSPECTED.items():
  print(f'{k}:{v}')

results = sorted(list(INSPECTED.values()))
print(f'{results[-1] * results[-2]}')
