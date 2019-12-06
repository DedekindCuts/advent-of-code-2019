class Object():
  def __init__(self, name):
    self.name = name
    self.parent = None

  def addParent(self, parent):
    self.parent = parent

  def getParent(self):
    return self.parent

  def getAncestors(self):
    ancestors = []
    x = self.getParent()
    while x is not None:
      ancestors.append(x)
      x = x.getParent()
    return ancestors

def minTransfers(a, b):
  """
  Calculate the minimum number of orbital transfers to move from the object 'a' 
  is orbiting to the object 'b' is orbiting
  """
  ancestors = {x:x.getAncestors() for x in (a,b)}
  common = set.intersection(*[set(ancestors[x]) for x in (a,b)])

  closest = {x:float('inf') for x in (a,b)}
  for c in common:
    closest = {x:min(closest[x], ancestors[x].index(c)) for x in (a,b)}

  return sum([closest[x] for x in (a,b)])

objects = {}
with open("06/input.txt") as input_file:
  for line in input_file:
    (p, c) = tuple(line.rstrip('\n').split(')'))
    for x in (p, c):
      if x not in objects:
        objects[x] = Object(x)
    objects[c].addParent(objects[p])

orbits = 0
for obj in objects:
  x = objects[obj]
  while x.getParent() is not None:
    orbits += 1
    x = x.getParent()

print(f"Total number of orbits: {str(orbits)}")

min_transfers = str(minTransfers(objects["YOU"], objects["SAN"]))
print(f"Minimum number of transfers required: {min_transfers}")
