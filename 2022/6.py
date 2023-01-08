input_file = '/Users/markeccles/adventcode/elves_6.txt'

X = [line for line in open(input_file)]

print(X[0])


input = X[0]
for i in range(4, len(input)):
  if len(set(input[i-4:i])) == 4:
    print(i)
    break

for i in range(14, len(input)):
  if len(set(input[i-14:i])) == 14:
    print(i)
    break