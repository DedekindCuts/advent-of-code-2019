class IntcodeMem(list):
  def __setitem__(self, index, value):
    """
    An Intcode memory object: a list which expands with 0s when necessary
    """
    missing = index - len(self) + 1
    self.extend([0] * missing)
    list.__setitem__(self, index, value)

class Intcode():
  def __init__(self, mem = IntcodeMem()):
    self.mem = mem
    self.pos = 0
    self.rel_base = 0
    self.halted = False
    self.output = None

    self.n_params = {1:3,2:3,3:1,4:1,5:2,6:2,7:3,8:3,9:1,99:0} # {opcode: # of parameters}
    self.assign_opcodes = [1, 2, 3, 7, 8] # opcodes which write to memory

  def _get_params(self, raw_params, param_modes):
    params = []
    for j in range(len(raw_params)):
      if j >= len(param_modes):
        mode = 0
      else:
        mode = param_modes[j]

      if mode == 0:
        if raw_params[j] >= len(self.mem):
          params.append(0)
        else:
          params.append(self.mem[raw_params[j]])
      elif mode == 1:
        params.append(raw_params[j])
      elif mode == 2:
        if self.rel_base + raw_params[j] >= len(self.mem):
          params.append(0)
        else:
          params.append(self.mem[self.rel_base + raw_params[j]])
      else:
        ValueError("Invalid parameter mode: " + mode)
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
    print(str(output))
    return output

  def execute(self, inputs = None):
    i = 0
    while True:
      (opcode, param_modes) = self._get_instruction(self.mem[self.pos])

      n = self.n_params[opcode]
      raw_params = [self.mem[self.pos+j+1] for j in range(n)]
      params = self._get_params(raw_params, param_modes)

      if opcode in self.assign_opcodes:
        if len(param_modes) < n:
          assign_index = self.mem[self.pos+n]
        else:
          if param_modes[n-1] == 2:
            assign_index = self.rel_base + self.mem[self.pos+n]
          else:
            raise ValueError(f"Invalid parameter mode: {param_modes[n-1]}")
      
      if opcode == 1:
        self.mem[assign_index] = params[0] + params[1]
      elif opcode == 2:
        self.mem[assign_index] = params[0] * params[1]
      elif opcode == 3:
        if inputs is None:
          ipt = self._get_input()
        elif i >= len(inputs):
          break # wait for further input
        else:
          ipt = inputs[i]
          i += 1
        self.mem[assign_index] = ipt
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
        self.mem[assign_index] = int(params[0] < params[1])
      elif opcode == 8:
        self.mem[assign_index] = int(params[0] == params[1])
      elif opcode == 9:
        self.rel_base += params[0]
      elif opcode == 99:
        self.halted = True
        break
      else:
        raise ValueError(str(opcode) + ' not a valid opcode')
      self.pos += n+1

with open("09/input.txt") as input_file:
  text = input_file.read().rstrip('\n')
  mem = IntcodeMem([int(x) for x in text.split(',')])

prog = Intcode(mem.copy())
prog.execute()
