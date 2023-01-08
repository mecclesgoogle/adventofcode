input_file = '/Users/markeccles/adventcode/2022/elves_7.txt'

f = open(input_file, 'r')

class File:
  def __init__(self, name, size):
    self.name = name
    self.size = size

class Dir:
  def __init__(self, name, parent_dir):
    self.name=name
    self.parent_dir = parent_dir
    self.dirs = []
    self.files = []
  
  def add_subdir(self, name):
    self.dirs.append(Dir(name, self))

  def add_file(self, name, size):
    self.files.append(File(name, size))

  def sub_dir(self, name):
    for dir in self.dirs:
      if dir.name == name:
        return dir
    raise ValueError(f'Dir {name} isn\'t a valid sub directory')

  def size(self):
    return sum([f.size for f in self.files]) + sum([d.size() for d in self.dirs])

# Globals
root_dir = Dir('/', None)
current_dir = root_dir

for line in f:
  line = line.strip()
  parts = line.split(' ')
  if parts[0] == '$':
    if 'cd' in line:
      name = parts[2]
      current_dir = current_dir.parent_dir if name == '..' else root_dir if name == '/' else current_dir.sub_dir(name)
  else:
    # we are inside an ls
    ls_parts = line.split(' ')
    if ls_parts[0] == 'dir':
      current_dir.add_subdir(ls_parts[1])
    else:
      current_dir.add_file(ls_parts[1], int(ls_parts[0]))

max_size = 100000

def calculate_sizes(dir, max_size):
  s = dir.size()
  e = s if s <= max_size else 0
  
  for subdir in dir.dirs:
    e += calculate_sizes(subdir, max_size)
  
  return e

print(calculate_sizes(root_dir, max_size))

# Part 2

space_need_to_free = 30000000 - 70000000 + root_dir.size()

def find_smallest(dir, min_size=space_need_to_free):
  s = dir.size()
  e = s if s >= min_size else 70000000
  
  for subdir in dir.dirs:
    e = min(e, find_smallest(subdir))

  return e

print(find_smallest(root_dir))