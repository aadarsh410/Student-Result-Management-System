import sqlite3


def create_database():
    from database import get_connection

    con = get_connection()

    # ---------------- Course Table ----------------
    con.execute("""
    CREATE TABLE IF NOT EXISTS course (
        cid INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        duration TEXT,
        charges TEXT,
        description TEXT
    )
    """)

    # ---------------- Student Table ----------------
    con.execute("""
    CREATE TABLE IF NOT EXISTS student (
        roll TEXT PRIMARY KEY,
        name TEXT,
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

    # ---------------- Result Table ----------------
    con.execute("""
    CREATE TABLE IF NOT EXISTS result (
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


if __name__ == "__main__":
    create_database()