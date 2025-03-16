import sqlite3 
import pandas as pd


def add_book(title, author, genre, year, read_status):
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Books (title, author, genere, year, read_status) VALUES (?, ?, ?, ?, ?)", 
                   (title, author, genre, year, read_status))
    conn.commit()
    conn.close()

def fetch_books():
    conn = sqlite3.connect("lib.db")
    df = pd.read_sql("SELECT * FROM Books", conn)
    conn.close()
    return df

def remove_book(book_id):
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Books WHERE book_id=?", (book_id,))
    conn.commit()
    conn.close()

def search_books(query):
    conn = sqlite3.connect("lib.db")
    df = pd.read_sql(f"SELECT * FROM Books WHERE title LIKE '%{query}%' OR author LIKE '%{query}%' OR genere LIKE '%{query}%'", conn)
    conn.close()
    return df

def book_statistics():
    conn = sqlite3.connect("lib.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM Books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Books WHERE read_status=1")
    read_books = cursor.fetchone()[0]

    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0

    conn.close()
    return total_books, read_books, percentage_read
