import sqlite3

DB_PATH = "ocr_results.db"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY,
    item_name TEXT,
    carbon_footprint REAL,
    quantity INTEGER,
    category TEXT,
    current_date TEXT
)
''')
conn.commit()

def run_sql(query: str):
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        return f"SQLite error: {e}"