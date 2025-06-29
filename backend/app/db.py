import sqlite3

def get_connection():
    return sqlite3.connect("readly.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pdf_path TEXT UNIQUE,
        pdf_name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        start_page INTEGER,
        end_page INTEGER,
        user_notes TEXT,
        reflection TEXT,
        date TEXT,
        FOREIGN KEY (book_id) REFERENCES books(id)
    )
    """)

    conn.commit()
    conn.close()


def reset_db():
    conn = sqlite3.connect("readly.db")
    cursor = conn.cursor()

    # Disable foreign key constraints (to avoid errors when deleting)
    cursor.execute("PRAGMA foreign_keys = OFF;")

    # Delete all data from tables
    cursor.execute("DELETE FROM books;")
    cursor.execute("DELETE FROM sessions;")

    # Reset auto-increment counters for SQLite
    cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name='books';")
    cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name='sessions';")

    # Re-enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")

    conn.commit()
    conn.close()
    print("Database reset successfully! All tables are now empty.")