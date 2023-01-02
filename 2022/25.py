import sys

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/25.txt'
X = [line.replace('\n','') for line in open(input_file)]

SNAFU_TO_B10 = {
  '0': 0,
  '1': 1,
  '2': 2,
  '-': -1,
  '=': -2, 
}

total = 0
for line in X:
  length = len(line)
  for i, c in enumerate(line):
    n = SNAFU_TO_B10[c]
    n *= 5 ** (length-i-1)
    total += n
  
# print(total)

B10_TO_SNAFU = {v: k for k, v in SNAFU_TO_B10.items()}
def b10_to_snafu(n: int):
  """Recursive conversion."""
  f = (n+2) // 5
  r = (n+2) % 5
  return '' if n == 0 else b10_to_snafu(f) + B10_TO_SNAFU[r-2]


print(b10_to_snafu(total))
