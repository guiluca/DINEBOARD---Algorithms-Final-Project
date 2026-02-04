# **DineBoard 🍽️**
## Restaurant Cost, Inventory, and Order Management System  

### Table of Contents

- Description
- Features
- Files Overview
- Prerequisites and Environment
- Installation and Execution
- Further Improvements
- Bibliography
- Credits

### Description📖

DineBoard is a simple Python-based system created to help small restaurant keep track of their ingredients, dishes, daily orders, costs, and inventory levels.

This project was designed to assist a small family restaurant (inspired by our groupmate's grandma’s business) in order to manage its expenses, keep track of ingredient stocks, and generate daily reports.

DineBoard allows users to:

- Add and manage ingredients with cost and quantity
- Create dishes with the ingredients added beforehand
- Record daily orders
- Automatically calculate daily expenses
- Track remaining stock and get low-stock alerts
- Store the date, dishes consumed, and daily expenses in a csv file
- Search previous records by date

### Features💡

Ingredient Management: Store ingredients with quantity and cost per unit.

Dish Builder: Combine ingredients to form recipes.

Daily Orders: Record daily orders and calculate expenses automatically.

Cost Tracking: Save daily data with detailed breakdowns to a CSV file.

Stock Tracker: Update and warn when ingredients are running low.

Date Search: Quickly find past order data using binary search by date.

Interactive Menu: Simple text-based interface that guides the user step-by-step.

### Files Overview📂

##### Ingredients.py:  

This was the first file created, and in simple terms, it allows users to input any ingredients needed for the operation of the restaurant, with its respective price and quantity. The main part of the code present in the file is to separate string inputs and convert them into base units so that our dictionary (that stores the ingredients) has a uniform design, allowing for further processing to be made. We also have a function that calculates the price per unit of ingredient.

##### Dishes.py:  

This was the second step of our code and very similarly to the ingredients python file, it allows the user to add a dish sold in the restaurant into a dictionary that will the be called later. We assume the user will only add ingredients added in the previous step, resulting on no need for an additional checker function at this stage.

##### Input_Checker.py:  

In the third step of our program, a checker function ensures that the dishes inputted by our users exist in the dishes dictionary previously created, and also, returns it in a format that is easier to process.

##### Cost_Tracker.py:  

This is the 4th step of our code and it basically creates a easy to access and follow database that tracks the daily expenses used in a specific day of operation. It adds the date, dish, quantity, cost per dish, and total cost of day into a csv file that can later be accessed by the manager of the restaurant. To do so the, a initial function first calculates the cost of each dish inputted by our user, by taking as input the "simply formatted inputs" from previous step and checking the dishes and inventory dictionaries from before. Then a secondary function multiplies the total cost of each inputted dish by the quantity ordered in the day and finally a third function adds it all to the csv file.

##### daily_orders_detailed.csv:  

A csv file that keeps track of the date, dish, quantity, cost per dish, and total cost of day for each day of operation.

##### Ingredient_Level.py:  

This file is responsible for taking as input the "simply formatted inputs" from "Input_Checker.py" and subtracting it from the current inventory level to output an updated amount of ingredients in the restaurant. A initial function calculates the inventory loss for the day and then another subtracts it rom the current inventory had, and also prints an alert if the original inventory (when it was first inputted) has reached 20% of its original amount.

##### Binary_Search.py:  

This file creates a binary search function that looks through the "daily_orders_detailed.csv" and returns the entry specified by the user in "O(log n)" running time.

##### USER.py:
This file is the only one the user should come in contact with, and it will be where the user can manage dishes, ingredients, orders and their expenses. It firstly ensures there is already a default dish (MVP dish) with 5 default ingredients (MVP ingredients) needed for it. Then, if the user runs the file a function called "main" runs and gives the user 7 actions that they can do: 1 - display current ingredients, 2 - display current dishes, 3 - Add new Ingredients, 4 - Add a new Dish, 5 - Record Daily orders, 6 - Search for a specific date and 7 - Exit the program. For selecting each of these options will call functions inside the file which import functions and databases from the other files to carry out that specific action.| 


### Prerequisites and Environment⚙️
- Python version: 3.10 or higher
- Libraries used: csv, datetime, and copy (all built-in python, no external packages needed)
- Developed on: Originally created on Google Colab, then transferred to Pycharm

### Installation and Execution🚀

#### Option A Pycharm + USER.py
This assumes the user has PyCharm or any other IDE that opens projects fully.

1. Download ZIP file from email
2. Right-click the ZIP and choose "extract-all". This will prompt you to select a folder
3. Choose the folder called "PycharmProjects", which usually is found in "This PC - OS(C:) - Users - <username> - PycharmProjects"
4. Open "Pycharm"
5. On the top left corner click on the "4 lines" next to the logo
6. Then click on "file" then "open"
7. Now follow the same path you did as before to find "PycharmProjects" and open "Dineboard"
8. Inside the "Dineboard" project/folder, open "USER.py" 
9. Click on the green play button
10. The terminal will open and now you should follow the program instructions
Extra 1: Before adding a new dish, make sure that you added the new ingredients needed.
Extra 2: Before searching for a date, make sure a daily order is inputted.

#### Option B Streamlit Web Interface
This runs Dineboard in a web browser removing the need for pycharm or any IDE.

1. Download the DineBoard ZIP file from email
2. Right-click on file and select "extract all"
3. Open the extracted DineBoard folder
4. Open Powershell in that folder
5. Create and activate a virtual environment (run "python -m venv .venv" and then ".venv\Scripts\activate")
6. install streamlit ("pip install streamlit")
7. Launch the web app (run "streamlit run app.py") and you'll be directed to the dashboard.


### Technical Highlights
- Clear separation of logic across multiple python files
- CSV data persistence 
- Inventory tracking
- Historical queries using Binary Search (O(log n))

### Further Improvements🔧
Dineboard can successfully manage ingredient tracking, calculation of costs, and create daily reports. However, there is always room for improvement, some potential ones being:
- Including a revenue and profit tracking feature, we would have to incorporate dish prices and quantities sold, this would make Dineboard an accounting assistant instead of just an expense tracker.
- Implementing an sql database (SQLite) would allow for advanced querying and make Dineboard scalable. 

### Bibliography📚
Readme file was based on: 
https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/

### Credits👥
Project Title: DineBoard

Developed by: Salim Cherraj, Sergio Daniel de los Reyes, Iñigo Gonzalez, Ander Krause, Guilherme Monteiro, David Villegas, and Jin Hui Zhao

Course: Algorithms and Data Structures

Instructor: Alejandro Martinez Mingo

Institution: IE University