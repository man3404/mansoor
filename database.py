import sqlite3

DB_NAME = "mansoor.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # للحصول على نتائج كقواميس
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Mass (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            apartment_number TEXT,
            apartment_type TEXT,
            building_name TEXT,
            tenant_name TEXT,
            rent_amount REAL,
            rent_type TEXT,
            rent_date TEXT,
            payment_date TEXT,
            phone_number TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()