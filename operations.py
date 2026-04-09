import sqlite3
import pandas as pd
import sqlite3

def export_to_csv():
    conn = sqlite3.connect("expenses.db")
    df = pd.read_sql_query("SELECT * FROM transactions", conn)

    df.to_csv("expenses.csv", index=False)
    conn.close()

def add_transaction(amount, t_type, category, date, desc):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions (amount, type, category, date, description)
    VALUES (?, ?, ?, ?, ?)
    """, (amount, t_type, category, date, desc))

    conn.commit()
    conn.close()


def view_transactions():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    conn.close()
    return rows


def monthly_summary(month):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT type, SUM(amount)
    FROM transactions
    WHERE strftime('%m', date) = ?
    GROUP BY type
    """, (month,))

    data = cursor.fetchall()
    conn.close()
    return data


def category_summary():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT category, SUM(amount)
    FROM transactions
    WHERE type='expense'
    GROUP BY category
    """)

    data = cursor.fetchall()
    conn.close()
    return data

def insights():
    conn = sqlite3.connect("expenses.db")
    df = pd.read_sql_query("SELECT * FROM transactions", conn)

    total_expense = df[df['type']=='expense']['amount'].sum()
    total_income = df[df['type']=='income']['amount'].sum()

    top_category = (
        df[df['type']=='expense']
        .groupby('category')['amount']
        .sum()
        .idxmax()
    )

    print(f"Total Income: {total_income}")
    print(f"Total Expense: {total_expense}")
    print(f"Top Spending Category: {top_category}")

    conn.close()

def spending_analysis():
    conn = sqlite3.connect("expenses.db")
    df = pd.read_sql_query("SELECT * FROM transactions", conn)

    expense_df = df[df['type']=='expense']
    total = expense_df['amount'].sum()

    grouped = expense_df.groupby('category')['amount'].sum()

    for cat, amt in grouped.items():
        percent = (amt / total) * 100
        print(f"{cat}: {percent:.2f}%")

    conn.close()