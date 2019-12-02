def execute(prog):
  """
  Function to execute Intcode program
  """
  i = 0
  while prog[i] != 99:
    if prog[i] == 1:
      prog[prog[i+3]] = prog[prog[i+1]] + prog[prog[i+2]]
      i += 4
    elif prog[i] == 2:
      prog[prog[i+3]] = prog[prog[i+1]] * prog[prog[i+2]]
      i += 4
    else:
      print('error: prog[' + str(i) + '] == ' + str(prog[i]))
      break
  return(prog)

with open("02/input.txt") as input_file:
  text = input_file.read().rstrip('\n')

mem_orig = [int(x) for x in text.split(',')]
mem = mem_orig.copy()

# restore program to "1202 program alarm" state
mem[1] = 12
mem[2] = 2

# execute program and show value in position 0
result = execute(mem)
print("Position 0: " + str(result[0]))

# check which values at positions 1 and 2 produce the desired output
for i in range(100):
  for j in range(100):
    mem = mem_orig.copy()
    mem[1] = i
    mem[2] = j
    result = execute(mem)[0]
    if result == 19690720:
      print("noun: " + str(i))
      print("verb: " + str(j))
      print("100 * noun + verb = " + str((100 * i) + j))
