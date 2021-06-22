from math import gcd

def subtract(a, b):
  """Returns a-b where a and b are tuples"""
  return tuple(x-y for x,y in zip(a,b))

def add(a, b):
  """Returns a+b where a and b are tuples"""
  return tuple(x+y for x,y in zip(a,b))

def GCD(numbers):
  """Finds the GCD of a list or tuple of at least 2 integers"""
  if len(numbers) < 2:
    raise ValueError("Need at least 2 numbers")
  result = numbers[0]
  for x in numbers:
    result = gcd(result, x)
  return result

def isvisible(a, b, ast_map):
  """Indicates whether b is visible to a, according to 'ast_map'"""
  if ast_map[a] == "." or ast_map[b] == ".":
    return False
  else:
    if a == b:
      return False
    else:
      rel_pos = subtract(b,a)
      fac = GCD(rel_pos)
      if fac == 1:
        return True
      else:
        rel_short = tuple(x//fac for x in rel_pos)
        for i in range(1, fac):
          coord = add(a, tuple(x*i for x in rel_short))
          if ast_map[coord] == ".":
            continue
          else:
            return False
        return True

def get_targets(pos, ast_map):
  """
  Returns a list of positions of asteroids that are in range of a laser at 
  'pos' in clockwise order starting directly above 'pos'
  """
  above = [x for x in ast_map if x[0] == pos[0] and x[1] < pos[1]]
  right = [x for x in ast_map if x[0] > pos[0]]
  below = [x for x in ast_map if x[0] == pos[0] and x[1] > pos[1]]
  left = [x for x in ast_map if x[0] < pos[0]]

  right.sort(key=lambda x: (x[1]-pos[1])/(x[0]-pos[0]))
  left.sort(key=lambda x: (x[1]-pos[1])/(x[0]-pos[0]))

  targets = above + right + below + left
  targets = [x for x in targets if isvisible(pos, x, ast_map)]
  
  return targets

with open('10/input.txt') as input_file:
  ipt = [line.rstrip('\n') for line in input_file]

AsteroidMap = {}
for y in range(len(ipt)):
  for x in range(len(ipt[y])):
    AsteroidMap[(x,y)] = ipt[y][x]

visible = {a:0 for a in AsteroidMap}
for a in AsteroidMap:
  for b in AsteroidMap:
    visible[a] += 1 if isvisible(a, b, AsteroidMap) else 0

most_visible = max([visible[a] for a in visible])
best_pos = [a for a in visible if visible[a] == most_visible][0]

print(f"Best position: {best_pos} with {most_visible} asteroids visible")

destroyed = []
while True:
  targets = get_targets(best_pos, AsteroidMap)
  if len(targets) == 0:
    break
  for target in targets:
    AsteroidMap[target] = "."
    destroyed.append(target)

print(f"200th asteroid destroyed: {destroyed[200-1]}")
