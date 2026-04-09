import sqlite3

print("Creating database...")

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")

def create_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    # Transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        type TEXT,
        category TEXT,
        date TEXT,
        description TEXT
    )
    """)

    # Users table ✅ FIXED
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

def register(username, password):
    import sqlite3

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        print("✅ User registered successfully")

    except sqlite3.IntegrityError:
        print("❌ Username already exists")

    conn.close()

def login(username, password):
    import sqlite3

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    return user  # ✅ IMPORTANT