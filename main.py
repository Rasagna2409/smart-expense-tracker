from database import create_db, register, login
from operations import *
from visualize import category_chart

# Create database & tables
create_db()

# 🔐 LOGIN / REGISTER
print("1. Login")
print("2. Register")

choice = input("Enter choice: ")

if choice == "2":
    u = input("Username: ")
    p = input("Password: ")
    register(u, p)
    print("✅ Registered successfully. Please login again.")
    exit()

elif choice == "1":
    u = input("Username: ")
    p = input("Password: ")
    
    if login(u, p):
        print("✅ Login successful")
    else:
        print("❌ Invalid credentials")
        exit()

# 🔁 MAIN MENU
while True:
    print("\n===== Expense Tracker =====")
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. Monthly Summary")
    print("4. Category Summary")
    print("5. Exit")
    print("6. Show Graph")
    print("7. Export to CSV")
    print("8. Smart Insights")

    choice = input("Enter choice: ")

    if choice == "1":
        amt = float(input("Amount: "))
        t = input("Type (income/expense): ")
        cat = input("Category: ")
        date = input("Date (YYYY-MM-DD): ")
        desc = input("Description: ")

        add_transaction(amt, t, cat, date, desc)
        print("✅ Added successfully")

    elif choice == "2":
        data = view_transactions()
        for row in data:
            print(row)

    elif choice == "3":
        month = input("Enter month (MM): ")
        data = monthly_summary(month)
        print("📊 Monthly Summary:", data)

    elif choice == "4":
        data = category_summary()
        print("📂 Category Summary:", data)

    elif choice == "5":
        print("👋 Exiting...")
        break

    elif choice == "6":
        category_chart()

    elif choice == "7":
        export_to_csv()
        print("✅ Data exported to expenses.csv")

    elif choice == "8":
        insights()

    else:
        print("❌ Invalid choice, try again")