import sqlite3

# =====================================================
# Result Management System Database Configuration
# =====================================================

DB_NAME = "result_management.db"


def get_connection():
    """
    Returns a connection to the project's database.
    """
    return sqlite3.connect(DB_NAME)


def initialize_database():
    """
    Creates all required tables if they don't already exist.
    This function is safe to call every time the application starts.
    """

    con = get_connection()
    cur = con.cursor()

    # =====================================================
    # Users Table
    # =====================================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # =====================================================
    # Student Table
    # =====================================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student(
            roll TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            gender TEXT,
            dob TEXT,
            contact TEXT,
            admission TEXT,
            course TEXT,
            state TEXT,
            city TEXT,
            pin TEXT,
            address TEXT
        )
    """)

    # =====================================================
    # Course Table
    # =====================================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course(
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            duration TEXT,
            charges TEXT,
            description TEXT
        )
    """)

    # =====================================================
    # Result Table
    # =====================================================
    cur.execute("""
CREATE TABLE IF NOT EXISTS result(
    roll TEXT PRIMARY KEY,
    name TEXT,
    course TEXT,
    marks TEXT,
    full_marks TEXT,
    percentage TEXT
)
""")

    con.commit()
    con.close()