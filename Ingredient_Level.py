# STEP 5 — Stock Level Tracker
# =======================================

# takes the daily order that will be inputed into the csv tracker and calculates the amount of ingredients used in that day

from Ingredients import parse_amount, to_base_units
from Dishes import dishes
from Input_Checker import input_day_orders

import copy


def day_ingredient_use(day_orders):
    """Return a dictionary with the total base-unit usage for each ingredient."""

    valid_orders = input_day_orders(day_orders)
    inv_loss = {}

    for dish_name, dishes_sold in valid_orders.items():
        recipe = dishes.get(dish_name)
        if not recipe:
            continue

        for ingredient_name, amount_str in recipe.items():
            value, unit = parse_amount(amount_str)
            base_value, _ = to_base_units(value, unit)
            inv_loss[ingredient_name] = inv_loss.get(ingredient_name, 0) + base_value * dishes_sold

    return inv_loss, valid_orders


# Function: takes the daily order and initial dictionary of igredients and subtracts them to have the remaining amouunt of ingredients left

def ingredient_tracker(current_ingredients, day_orders, original_stock):
    inv_loss, valid_orders = day_ingredient_use(day_orders)  # find how much ingredient was used

    copy_ingredients = copy.deepcopy(current_ingredients)  # creates a copy of original dictionary of ingredients to not change it
    warnings=[]

    for ingredient_name, used_amount in inv_loss.items():
        if ingredient_name not in copy_ingredients:
            continue

        current_value, unit = parse_amount(copy_ingredients[ingredient_name]["amount"])
        new_value = current_value - used_amount
        if new_value <= 0:
            new_value = 0

        copy_ingredients[ingredient_name]["amount"] = f"{new_value} {unit}"

    for ingredient_name, info in copy_ingredients.items():
        if ingredient_name not in original_stock:
            continue

        og_amount = parse_amount(original_stock[ingredient_name]["amount"])[0]
        if og_amount > 0:
            current_amount = parse_amount(info["amount"])[0]
            per_cent = current_amount / og_amount
            if per_cent <= 0.2:
                warnings.append(f"You must reorder {ingredient_name} (only {per_cent * 100:.1f}% left)")

    return copy_ingredients, valid_orders, warnings  # returns the new uopdated dictionary and the valid orders processed


