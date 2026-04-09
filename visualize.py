import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def category_chart():
    conn = sqlite3.connect("expenses.db")
    df = pd.read_sql_query("SELECT category, amount FROM transactions WHERE type='expense'", conn)

    summary = df.groupby("category").sum()

    summary.plot(kind="pie", y="amount", autopct='%1.1f%%')
    plt.title("Category-wise Expenses")
    plt.show()

    conn.close()