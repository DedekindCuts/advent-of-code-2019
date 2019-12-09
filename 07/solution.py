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

def _get_params(prog, raw_params, param_modes):
  params = []
  for j in range(len(raw_params)):
    if j+1 > len(param_modes):
      params.append(prog[raw_params[j]])
    else:
      if param_modes[j] == 0:
        params.append(prog[raw_params[j]])
      elif param_modes[j] == 1:
        params.append(raw_params[j])
      else:
        ValueError("Invalid parameter mode: " + param_modes[j])
  return params

def _get_instruction(code):
  inst = str(code)
  if len(inst) > 2:
    opcode = int(inst[-2] + inst[-1])
    param_modes = [int(inst[-i]) for i in range(3, len(inst)+1)]
  else:
    opcode = code
    param_modes = []
    
  return (opcode, param_modes)

def _get_input():
  while True:
    try:
      ipt = int(input("Input: "))
    except ValueError:
      print("Input must be an integer")
      continue
    else:
      return ipt

def _output(output):
  return output

def execute(prog, inputs=None):
  """
  Function to execute Intcode program
  """

  # {opcode: # of parameters}
  n_params = {1:3,2:3,3:1,4:1,5:2,6:2,7:3,8:3}

  pos = 0
  i = 0
  while prog[pos] != 99:
    (opcode, param_modes) = _get_instruction(prog[pos])

    n = n_params[opcode]
    raw_params = [prog[pos+j+1] for j in range(n)]
    params = _get_params(prog, raw_params, param_modes)
    
    if opcode == 1:
      prog[prog[pos+n]] = params[0] + params[1]
    elif opcode == 2:
      prog[prog[pos+n]] = params[0] * params[1]
    elif opcode == 3:
      ipt = _get_input() if inputs is None else inputs[i]
      if inputs is None:
        ipt = _get_input()
      else:
        ipt = inputs[i]
        i += 1
      prog[prog[pos+n]] = ipt
    elif opcode == 4:
      return _output(params[n-1])
    elif opcode == 5:
      if params[0] != 0:
        pos = params[1]
        continue
    elif opcode == 6:
      if params[0] == 0:
        pos = params[1]
        continue
    elif opcode == 7:
      prog[prog[pos+n]] = int(params[0] < params[1])
    elif opcode == 8:
      prog[prog[pos+n]] = int(params[0] == params[1])
    else:
      raise ValueError(str(opcode) + ' not a valid opcode')
    pos += n+1
  pass

with open("07/input.txt") as input_file:
  text = input_file.read().rstrip('\n')
  mem_orig = [int(x) for x in text.split(',')]

n_amps = 5
signals = []
sequences = permutations(range(n_amps))
for seq in sequences:
  output = 0
  for i in seq:
    mem = mem_orig.copy()
    output = execute(mem, inputs=[i, output])
  signals.append(output)

max_signal = max(signals)
best_seq = sequences[signals.index(max_signal)]
print(f"Max thruster signal: {max_signal}")
print(f"Best sequence: {best_seq}")
