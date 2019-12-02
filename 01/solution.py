import math

def fuelCost(mass):
  """
  function to calculate fuel cost for a given mass
  """

  return (math.floor(mass / 3) - 2)

def trueFuelCost(mass):
  """
  function to calculate fuel cost for a given mass after taking mass of fuel 
  into account
  """

  total = 0
  cost = mass

  while True:
    cost = max(fuelCost(cost), 0)
    total += cost
    if cost == 0:
      break

  return total

with open("01/input.txt") as input_file:
  lines = [line.rstrip('\n') for line in input_file]

# calculate total fuel cost
masses = [int(line) for line in lines]
costs = [fuelCost(mass) for mass in masses]
total_cost = sum(costs)
print("Total cost: " + str(total_cost))

# calculate total fuel cost taking weight of fuel into account
true_costs = [trueFuelCost(mass) for mass in masses]
true_total_cost = sum(true_costs)
print("True total cost: " + str(true_total_cost))
