# STEP 4 — Cost Tracker
# =======================================
#
# This program creates (or updates) a CSV file to store information about the meals consume on a daily basis and the estimated daily cost
# that the consumption of those meals has for the restaurant

from Ingredients import parse_amount, ingredients, to_base_units
from Dishes import dishes
from Input_Checker import input_day_orders

def calculate_dish_cost(dish_name):
    #Function is designed to calculate the total cost of serving one dish
    #You input the name of the desired dish you want calculated
    #Output is the cost

    #For case insensitivity
    dish_name = dish_name.lower()

    #Set initial counter
    total_cost = 0.0

    # Loop through each ingredient in the dish recipe
    recipe = dishes.get(dish_name)
    if not recipe:
        print(f"Warning: Dish '{dish_name}' not found in recipes.")
        return 0.0

    for ingredient_name, amount_str in recipe.items():
        ingredient_name = ingredient_name.lower()

        # Check if we have ingredient
        if ingredient_name not in ingredients:
            print(f"Warning: Ingredient '{ingredient_name}' not found in inventory.")
            continue

        # Parse the amount needed
        needed_value, needed_unit = parse_amount(amount_str)

        # Convert to base units
        needed_base_value, needed_base_unit = to_base_units(needed_value, needed_unit)

        # Get the price per base unit from our ingredients inventory
        price_per_unit = ingredients[ingredient_name]["price_per_unit"]

        # Calculate cost: (amount needed) × (price per unit)
        ingredient_cost = needed_base_value * price_per_unit

        # Add to running total
        total_cost += ingredient_cost

    return round(total_cost, 2)

def calculate_daily_expenses(day_orders):
    #Calculate total expenses for all dishes in a day

    #Set initial counter
    total_expenses = 0.0

    # Loop through each dish ordered that day
    valid_orders = input_day_orders(day_orders)

    for dish_name, quantity in valid_orders.items():

        #Calculate cost of one serving
        dish_cost = calculate_dish_cost(dish_name)

        # Multiply by quantity ordered and add to daily total
        total_expenses += dish_cost * quantity

    return round(total_expenses, 2)



import csv
def save_daily_orders_detailed_csv(date_str, day_orders, filename="daily_orders_detailed.csv"):
 #saves date,dish,quantity,cost per dish, total cost for dish, and daily expenses
 #The arguments are the date in YYYY-MM-DD, the day_orders dictionary, and the name of the file we want to create

    # Calculate daily expenses
    valid_orders = input_day_orders(day_orders)
    daily_expenses = calculate_daily_expenses(valid_orders)

    # Check if file exists
    try:
        with open(filename, 'r') as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    # Open file in append mode
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write headers if new file
        if not file_exists:
            writer.writerow(["Date", "Dish", "Quantity", "Cost_Per_Dish",
                           "Total_Cost_For_Dish", "Daily_Expenses"])

        # Write one row per dish with detailed cost breakdown
        for dish_name, quantity in valid_orders.items():
            cost_per_dish = calculate_dish_cost(dish_name)  # Cost of one serving
            total_for_dish = cost_per_dish * quantity  # Total cost for this dish

            writer.writerow([
                date_str,
                dish_name,
                quantity,
                f"€{cost_per_dish:.2f}",
                f"€{total_for_dish:.2f}",
                f"€{daily_expenses:.2f}"
            ])


    return {
        "filename": filename,
        "date": date_str,
        "daily_expenses": daily_expenses,
        "rows_written": len(valid_orders),
    }

