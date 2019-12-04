def checkPassword(x):
  """Function to check if x is a valid password"""
  x_str = str(x)
  double = False

  if len(x_str) != n:
    return False
  if x < limits[0] or x > limits[1]:
    return False
  for i in range(n-1):
    if int(x_str[i]) > int(x_str[i+1]):
      return False
    elif int(x_str[i]) == int(x_str[i+1]):
      double = True
  
  return double

def checkPassword2(x):
  """Function to check if x is a valid password using the updated guidelines"""
  x_str = str(x)
  double = False

  if len(x_str) != n:
    return False
  if x < limits[0] or x > limits[1]:
    return False
  for i in range(n-1):
    if int(x_str[i]) > int(x_str[i+1]):
      return False
    if i == 0:
      if int(x_str[i]) == int(x_str[i+1]):
        if int(x_str[i+1]) == int(x_str[i+2]):
          pass
        else:
          double = True
    elif i == n-2:
      if int(x_str[i]) == int(x_str[i+1]):
        if int(x_str[i-1]) == int(x_str[i]):
          pass
        else:
          double = True
    else:
      if int(x_str[i]) == int(x_str[i+1]):
        if int(x_str[i-1]) == int(x_str[i]) or \
           int(x_str[i+1]) == int(x_str[i+2]):
          pass
        else:
          double = True
  
  return double

n = 6 # number of digits for password
limits = (284639, 748759) # limits for password

valid = [i for i in range(limits[0], limits[1]+1) if checkPassword(i)]
valid2 = [i for i in range(limits[0], limits[1]+1) if checkPassword2(i)]

print("Number of valid passwords in range: " + str(len(valid)))
print("Number of ACTUALLY valid passwords in range: " + str(len(valid2)))
