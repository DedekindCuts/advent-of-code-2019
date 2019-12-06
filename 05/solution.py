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
  print(str(output))

def execute(prog):
  """
  Function to execute Intcode program
  """

  # {opcode: # of parameters}
  n_params = {1:3,2:3,3:1,4:1,5:2,6:2,7:3,8:3}

  pos = 0
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
      ipt = _get_input()
      prog[prog[pos+n]] = ipt
    elif opcode == 4:
      _output(params[n-1])
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
  return(prog)

with open("05/input.txt") as input_file:
  text = input_file.read().rstrip('\n')

mem_orig = [int(x) for x in text.split(',')]
mem = mem_orig.copy()

# execute program
result = execute(mem)
