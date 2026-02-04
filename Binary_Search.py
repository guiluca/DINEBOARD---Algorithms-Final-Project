# STEP 6 — BINARY SEARCH BY DATE (simple)
# =======================================
# Assumes:
# - The dataset (list of rows) is already sorted by date ascending.
# - Each row is a dictionary or list where the date is accessible as row["Date"] or row[0].
# - The target date is provided in 'YYYY-MM-DD' format.
#
# Goal:
# - Find all entries that match the target date using binary search on the Date column.

import csv

from datetime import datetime


def parse_date(date_str):
# Convert a 'YYYY-MM-DD' string to a date object.
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def binary_search_by_date(filename, target_date_str):

# Perform binary search on a sorted list of rows by their 'Date' column.
# Returns a list of all rows that match the given date.

    with open(file=filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        data2 = list(reader)

    if len(data2) == 0:
        return []

    target_date = parse_date(target_date_str)

    start = 0
    end = len(data2) - 1
    found_index = None

    while start <= end:
        mid = (start + end) // 2
        mid_date = parse_date(data2[mid]["Date"])

        if mid_date == target_date:
            found_index = mid
            break
        elif mid_date < target_date:
            start = mid + 1
        else:
            end = mid - 1

    if found_index is None: # If not found, return list
        return []

    results = [data2[found_index]] # Expand to include all rows with the same date

    # Check previous rows
    i = found_index - 1
    while i >= 0 and parse_date(data2[i]["Date"]) == target_date:
        results.insert(0, data2[i])
        i -= 1

    # Check next rows
    j = found_index + 1
    while j < len(data2) and parse_date(data2[j]["Date"]) == target_date:
        results.append(data2[j])
        j += 1

    return results