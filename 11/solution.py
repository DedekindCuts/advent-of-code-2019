def add(a, b):
  """Returns a+b where a and b are tuples"""
  return tuple(x+y for x,y in zip(a,b))

class Intcode():
  def __init__(self, memory):
    self.memory = memory
    self.halted = False
    self.output = None

  def execute(self, inputs = None):
    if inputs is None:
      return 1
    else:
      return inputs[0]

class Robot():
  def __init__(self, facing = 0, pos = (0,0)):
    self.facing = facing
    self.pos = pos
    self.history = [self.pos]
  
  def look(self, surface):
    return surface[self.pos]

  def turn(self, cmd):
    if cmd == 0:
      self.facing = (self.facing-1)%len(directions)
    elif cmd == 1:
      self.facing = (self.facing+1)%len(directions)
    else:
      raise ValueError("Turn command input should be either 0 or 1")
    self.move()

  def move(self):
    self.pos = add(self.pos, directions[self.facing])
    self.history.append(self.pos)

  def paint(self, surface, color):
    surface[self.pos] = color
  
directions = [(0,1), (1,0), (0,-1), (-1,0)]

with open("11/input.txt") as input_file:
  mem = input_file.read().rstrip('\n')

brain = Intcode(mem.copy())
rob = Robot()
hull = {}

while not brain.halted:
  brain.execute([rob.look(hull)])
  rob.paint(hull, brain.output)
  brain.execute()
  rob.turn(brain.output)

print(f"Number of panels painted at least once: {len(set(rob.history))}")
