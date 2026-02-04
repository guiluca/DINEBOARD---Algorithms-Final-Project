# STEP 3 — Entry Checker
# =======================================

# This function checks for the entry made by the user and filters out what makes sense and doesn't


from Dishes import dishes

def input_day_orders(orders):       # function that takes the orders as a parameter

  day_orders = {}                   #   creates a dictionary that will store orders with respective quantities

  for name, qty in orders.items():  #   for each dish name and quantity of dish in the list of orders
    name = name.strip().lower()     #     we get name of the order

    if name not in dishes:          #     if the dish does not exist in the dishes
      continue                      #       we continue to the next dish on the list

    try:                            #     tries block of code that might fail
      q = float(qty)                #       converts the quantity to a float
    except ValueError:              #     if trying raises an error
      continue                      #       we continue to the next dish on the list

    if q > 0:                       #     if the quantity is greater than 0
      day_orders[name] = q          #       in the day_orders dictionary, we save the dish name and set its value to the quantity

  return day_orders                 #   it returns that day's orders


