import os

input_file = '/Users/markeccles/adventcode/2022/elves_3.txt'


def score(item:str) -> int:
  if item.islower():
    return ord(item)-ord('a') + 1
  return ord(item)-ord('A') + 27

def get_common_item(bag: str) -> str:
  halfway = int(len(bag)/2)
  c_1 = set(bag[0:halfway])
  c_2 = set(bag[halfway:])
  return c_1.intersection(c_2).pop()

# Part 1
T = 0
for line in open(input_file):
  T += score(get_common_item(line.strip()))

print(T)

# Part 2
T = 0
bags = [line.strip() for line in open(input_file)]
for i in range(0, len(bags), 3):
  b = set.intersection(
    set(bags[i]), 
    set(bags[i+1]), 
    set(bags[i+2])).pop()
  T += score(b)

print(T)