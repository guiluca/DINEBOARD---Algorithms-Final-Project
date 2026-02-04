# STEP 2 — Dictionary of All Dishes
# =======================================

# Allows the user to input any dish, the ingredients required to make it and their respective amounts


# Dictionary of dishes
dishes = {}

# Function to add a dish with its ingredients
def add_dish(dish_name, ingredient_list):
    dishes[dish_name.lower()] = ingredient_list


