import sqlite3
import Password as passwords
def register_member(name, email):
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Members (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()

def authenticate_member(name,email):
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name,email FROM Members WHERE email = ? LIMIT 1", (email,))
    result = cursor.fetchone()  # Get email if it exists

    conn.close()

    return result is not None  # Return True if email exists, else False
