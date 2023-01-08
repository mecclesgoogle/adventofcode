import re

input_file = '/Users/markeccles/adventcode/elves_5.txt'

X = [x for x in open(input_file)]

# find the first line beggining with ' '
# then get the index of each crate
# use a dict {num: items}

crates = {}

for line_num, line in enumerate(X):
  line = line.replace('\n', '')
  if line.startswith(' 1'):
    for i, char in enumerate(line):
      if char != ' ':
        crates[char] = []
        for y in range(line_num - 1, -1, -1):
          if X[y][i] == ' ':
            break
          crates[char].append(X[y][i])
    print(f'original crates: {crates}')
  
  
  if line.startswith('move'):
    numbers = re.findall(r'\d+', line)
    q = int(numbers[0])
    f = numbers[1]
    t = numbers[2]
    for i in range(0, q):
      crates[t].append(crates[f].pop())

for v in crates.values():
  print(v.pop())


# PART 2
crates = {}
for line_num, line in enumerate(X):
  line = line.replace('\n', '')
  if line.startswith(' 1'):
    for i, char in enumerate(line):
      if char != ' ':
        crates[char] = []
        for y in range(line_num - 1, -1, -1):
          if X[y][i] == ' ':
            break
          crates[char].append(X[y][i])
    print(f'original crates: {crates}')
  
  
  if line.startswith('move'):
    numbers = re.findall(r'\d+', line)
    q = int(numbers[0])
    f = numbers[1]
    t = numbers[2]
    tmp = []
    for i in range(0, q):
      tmp.append(crates[f].pop())
    tmp.reverse()
    print(tmp)
    crates[t] = crates[t] + tmp

print(crates)

for v in crates.values():
  print(v.pop())