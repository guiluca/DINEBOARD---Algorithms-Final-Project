"""Interactive entry point for managing dishes, ingredients, and orders."""

import copy
from datetime import date

from Cost_Tracker import calculate_daily_expenses, save_daily_orders_detailed_csv
from Dishes import add_dish, dishes
from Ingredient_Level import ingredient_tracker
from Ingredients import add_ingredient, ingredients
from Input_Checker import input_day_orders
from Binary_Search import binary_search_by_date

def add_default_data():
    """Populate the system with a sample menu and inventory if empty."""

    if not ingredients:
        add_ingredient("noodles", "20 kg", 60.0)
        add_ingredient("chicken", "10 kg", 90.0)
        add_ingredient("carrot", "50 units", 20.0)
        add_ingredient("broccoli", "10 kg", 30.0)
        add_ingredient("bell pepper", "10 kg", 40.0)

    if not dishes:
        add_dish(
            "stir fry noodles",
            {
                "noodles": "200 g",
                "chicken": "100 g",
                "carrot": "1 unit",
                "broccoli": "50 g",
                "bell pepper": "40 g",
            },
        )


def display_ingredients():
    print("\nCURRENT INGREDIENT INVENTORY:")
    if not ingredients:
        print("  (no ingredients recorded)")
        return

    for name, data in ingredients.items():
        amount = data["amount"]
        cost = data["total_cost"]
        price = data["price_per_unit"]
        unit = data["price_unit_label"]
        print(f"  - {name.title()}: {amount}, €{cost:.2f} total (€/ {unit}: {price:.2f})")


def display_dishes():
    print("\nDISHES AND RECIPES:")
    if not dishes:
        print("  (no dishes recorded)")
        return

    for dish_name, recipe in dishes.items():
        formatted = ", ".join(f"{ing} -> {amount}" for ing, amount in recipe.items())
        print(f"  - {dish_name.title()}: {formatted}")


def user_add_ingredient(current_inventory, original_stock):
    print("\nAdd a new ingredient to the inventory")
    name = input("Ingredient name: ").strip().lower()
    if not name:
        print("Ingredient name cannot be empty.")
        return current_inventory, original_stock

    amount_str = input("Amount (e.g. '2 kg', '500 g', '10 units'): ").strip().lower()
    if not amount_str:
        print("Amount cannot be empty.")
        return current_inventory, original_stock

    try:
        total_cost = float(input("Total cost (€): ").strip())
    except ValueError:
        print("Invalid cost. Ingredient not added.")
        return current_inventory, original_stock

    add_ingredient(name, amount_str, total_cost)
    key = name.lower()
    current_inventory[key] = ingredients[key]
    original_stock[key] = ingredients[key]
    print(f"Ingredient '{name}' recorded.")
    return current_inventory, original_stock


def user_add_dish():
    print("\nAdd a new dish to the menu")
    dish_name = input("Dish name: ").strip().lower()
    if not dish_name:
        print("Dish name cannot be empty.")
        return

    if dish_name in dishes:
        print("Dish already exists. It will be overwritten with the new recipe.")

    print("Enter the ingredients required. Leave the ingredient name empty to finish.")
    recipe = {}
    while True:
        ingredient_name = input("Ingredient name: ").strip().lower()
        if ingredient_name == "":
            break
        amount = input("Amount needed (e.g. '200 g'): ").strip().lower()
        if not amount:
            print("Amount cannot be empty.")
            continue
        recipe[ingredient_name] = amount

    if not recipe:
        print("No ingredients provided. Dish not added.")
        return

    add_dish(dish_name, recipe)
    print(f"Dish '{dish_name}' saved with {len(recipe)} ingredients.")


def prompt_orders():
    print("\nEnter today's orders. Leave the dish name empty to finish.")
    orders = {}
    while True:
        dish_name = input("Dish name: ").strip()
        if dish_name == "":
            break
        quantity = input("Quantity sold: ").strip()
        if not quantity:
            print("Quantity cannot be empty. Try again.")
            continue
        orders[dish_name] = quantity
    return orders


def handle_daily_orders(current_inventory, original_stock):
    if not dishes:
        print("No dishes available. Please add dishes first.")
        return current_inventory

    orders = prompt_orders()
    if not orders:
        print("No orders recorded.")
        return current_inventory

    valid_orders = input_day_orders(orders)
    if not valid_orders:
        print("No valid orders after validation. Nothing to process.")
        return current_inventory

    expenses = calculate_daily_expenses(valid_orders)
    print(f"Total expenses for the day: €{expenses:.2f}")


    updated_inventory, processed_orders, warnings = ingredient_tracker(
        current_inventory, valid_orders, original_stock
    )

    for msg in warnings:
        print(msg)

    if processed_orders:
        date_str = input("Date for the report (YYYY-MM-DD, leave blank for today): ").strip()
        if not date_str:
            date_str = date.today().isoformat()
        summary = save_daily_orders_detailed_csv(date_str, valid_orders)
        print(f"Detailed data saved to {summary['filename']}")
        print(f"Date: {summary['date']}")
        print(f"Total Expenses: €{summary['daily_expenses']:.2f}")

    return updated_inventory


def menu():
    print(
        """
================= RESTAURANT OPERATIONS =================
1. View ingredients
2. View dishes
3. Add ingredient
4. Add dish
5. Record daily orders
6. Search for a specific data
7. Exit
=========================================================
"""
    )


def main():
    add_default_data()
    original_stock = copy.deepcopy(ingredients)
    current_inventory = copy.deepcopy(ingredients)

    print("Welcome to the restaurant management interface!")

    while True:
        menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            display_ingredients()
        elif choice == "2":
            display_dishes()
        elif choice == "3":
            current_inventory, original_stock = user_add_ingredient(
                current_inventory, original_stock
            )
        elif choice == "4":
            user_add_dish()
        elif choice == "5":
            current_inventory = handle_daily_orders(current_inventory, original_stock)
        elif choice =="6":
            user_date = input("Enter date (YYYY-MM-DD): ").strip()
            results = binary_search_by_date("daily_orders_detailed.csv", user_date)  # data should be our csv
            if results:
                print("Entries found:")
                for row in results:
                    print(row)
            else:
                print("No entries found for that date.")
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
