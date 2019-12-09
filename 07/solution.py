def permutations(l):
  """
  Returns all possible permutations of a given list or of all values in a given 
  range
  """

  if isinstance(l, range):
    l = [i for i in l]
  if not isinstance(l, list):
    raise ValueError("Input must be a list")

  perms = []
  for i in range(len(l)):
    p = [l[i]]
    if len(l) == 1:
      perms.append(p)
    else:
      tails = permutations(l[0:i] + l[i+1:len(l)])
      for j in range(len(tails)):
        perms.append(p + tails[j])
  
  return perms

class Intcode():
  def __init__(self, mem = []):
    self.mem = mem
    self.pos = 0
    self.n_params = {1:3,2:3,3:1,4:1,5:2,6:2,7:3,8:3,99:0} # {opcode: # of parameters}
    self.halted = False
    self.output = None

  def _get_params(self, raw_params, param_modes):
    params = []
    for j in range(len(raw_params)):
      if j+1 > len(param_modes):
        params.append(self.mem[raw_params[j]])
      else:
        if param_modes[j] == 0:
          params.append(self.mem[raw_params[j]])
        elif param_modes[j] == 1:
          params.append(raw_params[j])
        else:
          ValueError("Invalid parameter mode: " + param_modes[j])
    return params

  def _get_instruction(self, code):
    inst = str(code)
    if len(inst) > 2:
      opcode = int(inst[-2] + inst[-1])
      param_modes = [int(inst[-i]) for i in range(3, len(inst)+1)]
    else:
      opcode = code
      param_modes = []
    return (opcode, param_modes)

  def _get_input(self):
    while True:
      try:
        ipt = int(input("Input: "))
      except ValueError:
        print("Input must be an integer")
        continue
      else:
        return ipt

  def _output(self, output):
    return output

  def execute(self, inputs = None):
    i = 0
    while True:
      (opcode, param_modes) = self._get_instruction(self.mem[self.pos])

      n = self.n_params[opcode]
      raw_params = [self.mem[self.pos+j+1] for j in range(n)]
      params = self._get_params(raw_params, param_modes)
      
      if opcode == 1:
        self.mem[self.mem[self.pos+n]] = params[0] + params[1]
      elif opcode == 2:
        self.mem[self.mem[self.pos+n]] = params[0] * params[1]
      elif opcode == 3:
        if inputs is None:
          ipt = self._get_input()
        elif i >= len(inputs):
          break # wait for further input
        else:
          ipt = inputs[i]
          i += 1
        self.mem[self.mem[self.pos+n]] = ipt
      elif opcode == 4:
        self.output = self._output(params[n-1])
      elif opcode == 5:
        if params[0] != 0:
          self.pos = params[1]
          continue
      elif opcode == 6:
        if params[0] == 0:
          self.pos = params[1]
          continue
      elif opcode == 7:
        self.mem[self.mem[self.pos+n]] = int(params[0] < params[1])
      elif opcode == 8:
        self.mem[self.mem[self.pos+n]] = int(params[0] == params[1])
      elif opcode == 99:
        self.halted = True
        break
      else:
        raise ValueError(str(opcode) + ' not a valid opcode')
      self.pos += n+1

with open("07/input.txt") as input_file:
  text = input_file.read().rstrip('\n')
  mem_orig = [int(x) for x in text.split(',')]

n_amps = 5

signals = []
sequences = permutations(range(n_amps))
for seq in sequences:
  ipt = 0
  controllers = [Intcode(mem_orig.copy()) for _ in range(n_amps)]
  for i in seq:
    controllers[i].execute(inputs=[i, ipt])
    ipt = controllers[i].output
  signals.append(ipt)

max_signal = max(signals)
best_seq = sequences[signals.index(max_signal)]
print(f"Max thruster signal: {max_signal}")
print(f"Best sequence: {best_seq}")

sequences = permutations(range(n_amps, 2*n_amps))
signals = []
for seq in sequences:
  controllers = [Intcode(mem_orig.copy()) for _ in range(n_amps)]
  ipt = 0
  # run each controller once to provide the phase setting and initial input
  for i in range(n_amps):
    controllers[i].execute(inputs=[seq[i], ipt])
    ipt = controllers[i].output
  contrl = 0
  halted = False
  # run each controller in succession until one halts
  while not halted:
    controllers[contrl].execute(inputs=[ipt])
    ipt = controllers[contrl].output
    contrl = (contrl+1)%5
    if controllers[contrl].halted:
      signals.append(ipt)
      halted = True
      break

max_signal = max(signals)
best_seq = sequences[signals.index(max_signal)]
print(f"Max thruster signal: {max_signal}")
print(f"Best sequence: {best_seq}")
