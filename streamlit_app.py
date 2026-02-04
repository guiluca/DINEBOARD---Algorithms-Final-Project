"""Streamlit web interface for restaurant management system."""

import streamlit as st
import pandas as pd
import copy
from datetime import date

from Cost_Tracker import calculate_daily_expenses, save_daily_orders_detailed_csv, calculate_dish_cost
from Dishes import add_dish, dishes
from Ingredient_Level import ingredient_tracker
from Ingredients import add_ingredient, ingredients
from Input_Checker import input_day_orders
from Binary_Search import binary_search_by_date


# Set up the page
st.set_page_config(
    page_title="Restaurant Manager",
    page_icon="🍽️",
    layout="wide"
)

#Set up session state (runs only once when app starts)
if 'initialized' not in st.session_state:
    # Add some default sample data
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

    #Save original stock amounts and current inventory
    st.session_state.original_stock = copy.deepcopy(ingredients)
    st.session_state.current_inventory = copy.deepcopy(ingredients)
    st.session_state.initialized = True


# Title
st.title("🍽️ Restaurant Management System")
st.markdown("---")

#Tabs to switch from one file to another
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "🥕 Ingredients",
    "🍜 Dishes",
    "📝 Daily Orders",
    "🔍 Search Records"
])


#Dashboard
with tab1:
    st.header("Dashboard Overview")

    #Key metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Ingredients", len(st.session_state.current_inventory))

    with col2:
        st.metric("Total Dishes", len(dishes))

    with col3:
        #Add up value of inventory
        total_value = sum(item['total_cost'] for item in st.session_state.current_inventory.values())
        st.metric("Inventory Value", f"€{total_value:.2f}")

    st.markdown("---")

    #Low stock warnings
    st.subheader("⚠️ Stock Alerts")
    warnings = []
    for ingredient_name, info in st.session_state.current_inventory.items():
        if ingredient_name not in st.session_state.original_stock:
            continue

        from Ingredients import parse_amount
        #Original amount
        og_amount = parse_amount(st.session_state.original_stock[ingredient_name]["amount"])[0]
        if og_amount > 0:
            #Current amount
            current_amount = parse_amount(info["amount"])[0]
            #Percentage
            per_cent = current_amount / og_amount
            # If below 20%, add to warnings
            if per_cent <= 0.2:
                warnings.append({
                    "Ingredient": ingredient_name.title(),
                    "Stock Level": f"{per_cent * 100:.1f}%",
                    "Current Amount": info["amount"]
                })

    if warnings:
        df_warnings = pd.DataFrame(warnings)
        st.error("🚨 Low Stock Alert - Reorder Required!")
        st.dataframe(df_warnings, use_container_width=True, hide_index=True)
    else:
        st.success("✅ All ingredients are well-stocked!")

    st.markdown("---")

    #Overview of inventory and dishes
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🥕 Current Inventory")
        if st.session_state.current_inventory:
            #Inventory table
            inv_data = []
            for name, data in st.session_state.current_inventory.items():
                inv_data.append({
                    "Ingredient": name.title(),
                    "Amount": data["amount"],
                    "Total Cost": f"€{data['total_cost']:.2f}",
                    "Price/Unit": f"€{data['price_per_unit']:.4f}/{data['price_unit_label']}"
                })
            df_inv = pd.DataFrame(inv_data)
            st.dataframe(df_inv, use_container_width=True, hide_index=True)
        else:
            st.info("No ingredients in inventory")

    with col2:
        st.subheader("🍜 Menu Items")
        if dishes:
            #Create list of dishes
            dish_data = []
            for dish_name, recipe in dishes.items():
                cost = calculate_dish_cost(dish_name)
                dish_data.append({
                    "Dish": dish_name.title(),
                    "Ingredients": len(recipe),
                    "Cost per Serving": f"€{cost:.2f}"
                })
            df_dishes = pd.DataFrame(dish_data)
            st.dataframe(df_dishes, use_container_width=True, hide_index=True)
        else:
            st.info("No dishes in menu")


#Ingredients
with tab2:
    st.header("Ingredient Management")

    #2 subtabs, view and add
    view_tab, add_tab = st.tabs(["📋 View Ingredients", "➕ Add Ingredient"])

    with view_tab:
        if st.session_state.current_inventory:
            #Create ingredient table
            inv_data = []
            for name, data in st.session_state.current_inventory.items():
                inv_data.append({
                    "Ingredient": name.title(),
                    "Amount": data["amount"],
                    "Total Cost": f"€{data['total_cost']:.2f}",
                    "Price per Unit": f"€{data['price_per_unit']:.4f}",
                    "Unit": data['price_unit_label']
                })
            df_inv = pd.DataFrame(inv_data)
            st.dataframe(df_inv, use_container_width=True, hide_index=True)
        else:
            st.info("No ingredients found. Add your first ingredient!")

    with add_tab:
        # Create ingredient form
        with st.form("add_ingredient_form"):
            st.subheader("Add New Ingredient")

            col1, col2 = st.columns(2)

            with col1:
                ing_name = st.text_input("Ingredient Name", placeholder="e.g., Tomatoes")
                ing_amount = st.text_input("Amount", placeholder="e.g., 5 kg or 10 units")

            with col2:
                ing_cost = st.number_input("Total Cost (€)", min_value=0.0, step=0.01, format="%.2f")

            #Form submit button
            submitted = st.form_submit_button("Add Ingredient", type="primary", use_container_width=True)

            if submitted:
                if not ing_name or not ing_amount:
                    st.error("Please fill in all fields!")
                else:
                    try:
                        #Add ingredient
                        add_ingredient(ing_name.lower(), ing_amount.lower(), ing_cost)
                        key = ing_name.lower()
                        st.session_state.current_inventory[key] = ingredients[key]
                        st.session_state.original_stock[key] = ingredients[key]
                        st.success(f"✅ Added '{ing_name}' to inventory!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding ingredient: {str(e)}")


#Dishes
with tab3:
    st.header("Dish & Recipe Management")

    #Create 2 subtabs
    view_tab, add_tab = st.tabs(["📋 View Dishes", "➕ Add Dish"])

    with view_tab:
        if dishes:
            #Show each dish
            for dish_name, recipe in dishes.items():
                with st.expander(f"🍽️ {dish_name.title()}", expanded=False):
                    cost = calculate_dish_cost(dish_name)
                    st.metric("Cost per Serving", f"€{cost:.2f}")

                    st.write("**Recipe:**")
                    recipe_data = []
                    for ing, amount in recipe.items():
                        recipe_data.append({"Ingredient": ing.title(), "Amount": amount})
                    df_recipe = pd.DataFrame(recipe_data)
                    st.dataframe(df_recipe, use_container_width=True, hide_index=True)
        else:
            st.info("No dishes found. Add your first dish!")

    with add_tab:
        st.subheader("Add New Dish")

        dish_name = st.text_input("Dish Name", placeholder="e.g., Caesar Salad")

        st.write("**Add Ingredients:**")

        #Ingredients for recipes
        if 'recipe_ingredients' not in st.session_state:
            st.session_state.recipe_ingredients = []

        #Form to add ingredients to the recipe
        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            new_ing = st.text_input("Ingredient", key="new_ing", placeholder="e.g., lettuce")
        with col2:
            new_amount = st.text_input("Amount", key="new_amount", placeholder="e.g., 100 g")
        with col3:
            if st.button("➕ Add", use_container_width=True):
                if new_ing and new_amount:
                    st.session_state.recipe_ingredients.append({
                        "ingredient": new_ing.lower(),
                        "amount": new_amount.lower()
                    })
                    st.rerun()

        #Shows current recipe
        if st.session_state.recipe_ingredients:
            st.write("**Current Recipe:**")
            for idx, item in enumerate(st.session_state.recipe_ingredients):
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.write(f"- {item['ingredient'].title()}: {item['amount']}")
                with col2:
                    #Button to remove this ingredient
                    if st.button("❌", key=f"remove_{idx}"):
                        st.session_state.recipe_ingredients.pop(idx)
                        st.rerun()

        #Save the dish
        if st.button("Save Dish", type="primary", use_container_width=True):
            if not dish_name:
                st.error("Please enter a dish name!")
            elif not st.session_state.recipe_ingredients:
                st.error("Please add at least one ingredient!")
            else:
                #Make dictionary
                recipe_dict = {item['ingredient']: item['amount'] for item in st.session_state.recipe_ingredients}
                add_dish(dish_name.lower(), recipe_dict)
                st.success(f"✅ Added '{dish_name}' to menu!")
                st.session_state.recipe_ingredients = []
                st.rerun()


#Daily Orders
with tab4:
    st.header("Record Daily Orders")

    if not dishes:
        st.warning("⚠️ No dishes available. Please add dishes first.")
    else:
        #Pick a date for the orders
        order_date = st.date_input("Order Date", value=date.today())

        st.subheader("Enter Orders")

        if 'daily_orders' not in st.session_state:
            st.session_state.daily_orders = {}

        #Add orders form
        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            #Dish selection
            dish_options = [d.title() for d in dishes.keys()]
            selected_dish = st.selectbox("Select Dish", dish_options, key="selected_dish")
        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1, key="quantity")
        with col3:
            if st.button("➕ Add Order", use_container_width=True):
                dish_key = selected_dish.lower()
                # If dish was already added, add to quantity
                if dish_key in st.session_state.daily_orders:
                    st.session_state.daily_orders[dish_key] += quantity
                else:
                    st.session_state.daily_orders[dish_key] = quantity
                st.rerun()

        #Show current orders
        if st.session_state.daily_orders:
            st.markdown("---")
            st.subheader("Today's Orders")

            #Build orders table
            order_data = []
            total_cost = 0
            for dish, qty in st.session_state.daily_orders.items():
                cost_per_dish = calculate_dish_cost(dish)
                total_for_dish = cost_per_dish * qty
                total_cost += total_for_dish
                order_data.append({
                    "Dish": dish.title(),
                    "Quantity": qty,
                    "Cost/Dish": f"€{cost_per_dish:.2f}",
                    "Total": f"€{total_for_dish:.2f}"
                })

            df_orders = pd.DataFrame(order_data)
            st.dataframe(df_orders, use_container_width=True, hide_index=True)

            st.metric("Total Daily Expenses", f"€{total_cost:.2f}")

            col1, col2 = st.columns([1, 1])
            with col1:
                #Clear all orders
                if st.button("🗑️ Clear Orders", use_container_width=True):
                    st.session_state.daily_orders = {}
                    st.rerun()

            with col2:
                #Process and save orders
                if st.button("💾 Save & Process Orders", type="primary", use_container_width=True):
                    #Validate orders
                    valid_orders = input_day_orders(st.session_state.daily_orders)

                    if valid_orders:
                        #Update inventory based on what was used
                        updated_inventory, processed_orders, warnings = ingredient_tracker(
                            st.session_state.current_inventory,
                            valid_orders,
                            st.session_state.original_stock
                        )

                        st.session_state.current_inventory = updated_inventory

                        #Save to CSV file
                        date_str = order_date.isoformat()
                        summary = save_daily_orders_detailed_csv(date_str, valid_orders)

                        st.success(f"✅ Orders processed and saved to {summary['filename']}")

                        #Show stock warnings
                        if warnings:
                            st.warning("⚠️ Stock Alerts:")
                            for warning in warnings:
                                st.write(f"- {warning}")

                        #Clear orders for next time
                        st.session_state.daily_orders = {}
                        st.rerun()
                    else:
                        st.error("No valid orders to process!")


# ==================== SEARCH RECORDS TAB ====================
with tab5:
    st.header("Search Order Records")

    #Pick a date
    search_date = st.date_input("Select Date", value=date.today())

    if st.button("🔍 Search", type="primary"):
        try:
            date_str = search_date.isoformat()
            #Search for records from this date
            results = binary_search_by_date("daily_orders_detailed.csv", date_str)

            if results:
                st.success(f"Found {len(results)} record(s) for {date_str}")

                #Show results in a table
                df_results = pd.DataFrame(results)
                st.dataframe(df_results, use_container_width=True, hide_index=True)

                #Show total expenses for the day
                if 'Daily_Expenses' in df_results.columns:
                    daily_total = df_results['Daily_Expenses'].iloc[0]
                    st.metric("Total Expenses for This Day", daily_total)
            else:
                st.info(f"No records found for {date_str}")

        except FileNotFoundError:
            st.error("No order records found. Process some orders first!")
        except Exception as e:
            st.error(f"Error searching records: {str(e)}")


# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Restaurant Management System v1.0</div>",
    unsafe_allow_html=True
)