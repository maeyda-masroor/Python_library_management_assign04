import sqlite3
import Password as passwords

def register_librarian(username, password):
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Lib (username, password) VALUES (?, ?)", (username, passwords.hash_password(password)))
    conn.commit()
    conn.close()

def authenticate_librarian(username, password):
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM Lib WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result and passwords.verify_password(password, result[0]):
        return True
    return False
