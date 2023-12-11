#QUICKADD Feature
#File is always reading home_input.txt. If the text is in the valid form of Expense, Amount, Month, Day, then the file will move that information to 
#track_expenses.json
import json


while True:
    possible_pages = ("GRAPHS", "EXPENSES", "EDIT", "BREAKDOWN", "HELP AND PATCH NOTES", "ABOUT US")

    with open('home_input.txt', 'r') as infile:
        #Makes sure the text file reads a valid quickadd input
        expense_input = infile.read()
        if expense_input and expense_input not in possible_pages:

            expense_input = expense_input.split(', ')

            category = expense_input[0]
            amount = expense_input[1]
            month = expense_input[2]
            day = expense_input[3]

            with open('track_expenses.json', 'r') as json_infile:
                expense_data = json.load(json_infile)

            new_expense = {"Category": category, 
                "Amount": amount,
                "Day": day}
            
            #Enter if user only gave a category and amount
            if month == "None" and day == "None":
                if "None" in expense_data:
                    expense_data["None"].append(new_expense)
                else: 
                    expense_data["None"] = [new_expense]
            
            elif month != "None":
                if month in expense_data:
                    expense_data[month].append(new_expense)
                else:  
                    expense_data[month] = [new_expense]

            #Update json file with old and new expense
            with open('track_expenses.json', 'w') as json_outfile:
                json.dump(expense_data, json_outfile, indent=2)

            print("Successfully added!")
            #Overwrite home_input.txt so we dont add the same thing over and over again to track_expenses.json
            with open('home_input.txt', 'w') as txt_outfile:
                pass

            
