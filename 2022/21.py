import sys
from sympy import symbols, solve

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/21.txt'
X = [line.strip() for line in open(input_file)]

def parse_line(line)-> dict:
  """Returns ma (name, number, expression(array))"""
  name = line[0:4]
  e = line.split(':')[1].strip()
  if e.isnumeric():
    return (name, int(e), None)
  else:
    return (name, None, e.split())
    
  
monkeys = {}
for line in X:
  m = parse_line(line)
  monkeys[m[0]] = (m[1], m[2])
  

def part1(monkeys, name):
  monkey = monkeys[name]
  if monkey[0] is not None:
    return monkey[0]
  (l, operator, r) = monkey[1]
  l = part1(monkeys, l)
  r = part1(monkeys, r)
  if operator == '+':
    return l + r
  elif operator == '-':
    return l - r
  elif operator == '*':
    return l * r
  elif operator == '/':
    return int(l / r)
    
print(part1(monkeys, 'root'))

def part2(monkeys, name):
  if name == 'humn':
    return 'x'
  
  monkey = monkeys[name]
  if monkey[0] is not None:
    return monkey[0]
    
  (l, operator, r) = monkey[1]
  l = part2(monkeys, l)
  r = part2(monkeys, r)

  if name == 'root':
    return f'{l} - {r}'
  
  if type(l) == str or type(r) == str:
    return f'({l} {operator} {r})'
  
  if operator == '+':
    return l + r
  elif operator == '-':
    return l - r
  elif operator == '*':
    return l * r
  elif operator == '/':
    return int(l / r)
  
expr = part2(monkeys, 'root')
x = symbols('x')
print(solve(expr)[0])
