# STEP 1 — Dictionary of Ingredients
# =======================================

# Allows the user to input any ingredient, with the respective quantity and cost to acquire
# Convert the units into base units used in our algorithms and calculates the price per unit of that ingredient



# Function: converts a string like "2 kg" into value + unit
def parse_amount(amount_str):
    parts = amount_str.strip().lower().split(" ")
    value = float(parts[0])   # Example: "2" becomes 2.0
    unit = parts[1]           # Example: "kg"
    return value, unit

# Function: converts to base units → grams for weight, unit for pieces
def to_base_units(value, unit):
    if unit == "kg":
        return value * 1000, "g"   # 1 kg = 1000 g
    elif unit == "g":
        return value, "g"
    elif unit == "unit" or unit == "units":
        return value, "unit"
    else:
        return value, unit   # fallback (not needed for now)

def format_amount(value, unit):
    # use integer formatting when possible
    if float(value).is_integer():
        return f"{int(value)} {unit}"
    return f"{value} {unit}"


# Function: compute price per base unit (€/g or €/unit)
def price_per_base_unit(total_cost, amount_str):
    value, unit = parse_amount(amount_str)
    base_value, base_unit = to_base_units(value, unit)
    return total_cost / base_value, base_unit


# Dictionary of ingredients
ingredients = {}

# Function to add an ingredient to the dictionary
def add_ingredient(name, amount_str, total_cost):
    ppu, base_unit = price_per_base_unit(total_cost, amount_str)  # ppu = price per unit (base)

    val, unit = parse_amount(amount_str)
    base_val, base_unit_for_amount = to_base_units(val, unit)
    amount_base_str = format_amount(base_val, base_unit_for_amount) # to have it in base units

    ingredients[name.lower()] = {
        "amount": amount_base_str,
        "total_cost": total_cost,
        "price_per_unit": ppu,
        "price_unit_label": base_unit
    }


