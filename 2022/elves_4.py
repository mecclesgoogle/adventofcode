input_file = '/Users/markeccles/adventcode/2022/elves_4.txt'


def one_contains_other(l1: list[str], l2: list[str]):
  return set(l1) <= set(l2) or set(l2) <= set(l1)


def extract_lists(line: str):
  line = line.strip()
  s = line.split(',')
  l1_range = s[0]
  l2_range = s[1]
  l1_start = int(l1_range.split('-')[0])
  l1_end = int(l1_range.split('-')[1])
  l2_start = int(l2_range.split('-')[0])
  l2_end = int(l2_range.split('-')[1])
  return [x for x in range(l1_start, l1_end+1)],[x for x in range(l2_start, l2_end+1)]

T = 0
for line in open(input_file, 'r'):
  (l1, l2) = extract_lists(line)
  T += 1 if one_contains_other(l1,l2) else 0

print(T)

# Part 2
def has_common_elements(l1: list[str], l2: list[str]):
  return len(set(l1).intersection(set(l2))) > 0

T = 0
for line in open(input_file, 'r'):
  (l1, l2) = extract_lists(line)

  T += 1 if has_common_elements(l1,l2) else 0

print(T)
