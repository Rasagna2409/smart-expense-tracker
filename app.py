import streamlit as st
import pandas as pd
import sqlite3
from operations import *
from database import create_db, register, login

# DB init
create_db()

st.set_page_config(page_title="Expense Tracker", layout="wide")

# ---------------- LOGIN SYSTEM ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.sidebar.title("🔐 Authentication")

auth = st.sidebar.selectbox("Choose", ["Login", "Register"])

if not st.session_state.logged_in:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if auth == "Register":
        if st.sidebar.button("Register"):
            register(username, password)
            st.sidebar.success("Registered! Now login.")

    elif auth == "Login":
        if st.sidebar.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    st.stop()

# ---------------- MAIN APP ----------------
st.title("💰 Smart Expense Tracker Dashboard")

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Add Transaction", "View Transactions"]
)

# Load data
conn = sqlite3.connect("expenses.db")
df = pd.read_sql_query("SELECT * FROM transactions", conn)
conn.close()

# ---------------- FILTERS ----------------
st.sidebar.subheader("📅 Filters")

if not df.empty:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])

    month = st.sidebar.selectbox("Month", ["All"] + list(df['date'].dt.month.unique()))
    year = st.sidebar.selectbox("Year", ["All"] + list(df['date'].dt.year.unique()))

    if month != "All":
        df = df[df['date'].dt.month == month]
    if year != "All":
        df = df[df['date'].dt.year == year]

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.subheader("📊 Overview")

    if df.empty:
        st.warning("No data available")
    else:
        total_income = df[df['type']=='income']['amount'].sum()
        total_expense = df[df['type']=='expense']['amount'].sum()
        balance = total_income - total_expense

        # KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Income", f"₹{total_income}")
        col2.metric("💸 Expense", f"₹{total_expense}")
        col3.metric("🏦 Balance", f"₹{balance}")

        # Layout
        col4, col5 = st.columns(2)

        # Pie Chart
        with col4:
            st.subheader("🥧 Category Distribution")
            expense_df = df[df['type']=='expense']
            if not expense_df.empty:
                pie = expense_df.groupby('category')['amount'].sum()
                st.pyplot(pie.plot.pie(autopct='%1.1f%%').figure)

        # Monthly Trend
        with col5:
            st.subheader("📈 Monthly Trend")
            monthly = df.groupby(df['date'].dt.to_period("M"))['amount'].sum()
            monthly.index = monthly.index.astype(str)
            st.line_chart(monthly)

        # ---------------- AI INSIGHTS ----------------
        st.subheader("🤖 AI Insights")

        if total_expense > total_income:
            st.error("⚠️ You are overspending!")

        top_category = (
            df[df['type']=='expense']
            .groupby('category')['amount']
            .sum()
            .idxmax()
        )

        st.info(f"💡 You spend most on **{top_category}**")

# ---------------- ADD ----------------
elif menu == "Add Transaction":
    st.subheader("➕ Add Transaction")

    amt = st.number_input("Amount", min_value=0.0)
    t = st.selectbox("Type", ["income", "expense"])
    cat = st.text_input("Category")
    date = st.date_input("Date")
    desc = st.text_input("Description")

    if st.button("Add"):
        if cat.strip() == "":
            st.error("Category required")
        else:
            add_transaction(amt, t, cat, str(date), desc)
            st.success("✅ Added Successfully")

# ---------------- VIEW ----------------
elif menu == "View Transactions":
    st.subheader("📄 Transactions")

    if df.empty:
        st.warning("No data available")
    else:
        st.dataframe(df)

        # ---------------- DOWNLOAD ----------------
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download CSV",
            data=csv,
            file_name="expenses.csv",
            mime="text/csv"
        )