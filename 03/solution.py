import math

def taxi_dist(a, b):
  """
  Manhattan (taxicab) distance between a and b, where a and b are n-tuples 
  representing Cartesian coordinates
  """
  for arg in [a, b]:
    if not isinstance(arg, tuple):
      TypeError("inputs must be tuples")

  if len(a) != len(b):
    ValueError("lengths of inputs must match")

  return sum([abs(a[i] - b[i]) for i in range(len(a))])

class Wire:
  def __init__(self, start):
    self.points = [start]
    self.end = start

  def addSubpath(self, subpath):
    direction = subpath[0]
    length = int(subpath[1:len(subpath)])

    if direction == "U":
      covered = [(self.end[0], self.end[1] + i) for i in range(1, length + 1)]
      self.end = (self.end[0], self.end[1] + length)
    elif direction == "D":
      covered = [(self.end[0], self.end[1] - i) for i in range(1, length + 1)]
      self.end = (self.end[0], self.end[1] - length)
    elif direction == "R":
      covered = [(self.end[0] + i, self.end[1]) for i in range(1, length + 1)]
      self.end = (self.end[0] + length, self.end[1])
    elif direction == "L":
      covered = [(self.end[0] - i, self.end[1]) for i in range(1, length + 1)]
      self.end = (self.end[0] - length, self.end[1])
    else:
      ValueError("\'" + direction + "\' not a valid direction")
    
    self.points += covered

  def getPoints(self):
    return set(self.points)

  def getSteps(self, point):
    return self.points.index(point)

with open("03/input.txt") as input_file:
  paths = [line.rstrip('\n').split(',') for line in input_file]

origin = (0,0)

wires = [Wire(origin) for _ in range(len(paths))]

for i in range(len(paths)):
  for subpath in paths[i]:
    wires[i].addSubpath(subpath)

overlaps = set.intersection(*[x.getPoints() for x in wires])
overlaps = {x for x in overlaps if x != origin}

distances = [taxi_dist(x, origin) for x in overlaps]
min_dist = min(distances)
print("Minimum distance from origin to intersection: " + str(min_dist))

steps = [sum([w.getSteps(x) for w in wires]) for x in overlaps]
min_steps = min(steps)
print("Least total steps to intersection: " + str(min_steps))
